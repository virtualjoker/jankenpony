# myapp.models.player
#
# model: Player
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from status import Status

from ..aux import serialize
from ..aux import deserialize

#
# When anonymous changes to a identifyed user, it isn't deleted from memory
# (should be reviewed)

class Player(db.Model):
  """ Player Model
      This model show the player properties and
      the methods to manipulate his properties
      
      Player should be take with get_current_player at begin
      and should be put at the end of every request that use it """
  
  #######################
  #  PUBLIC PROPERTIES  #
  #######################
  
  
  # The Google's user account is required
  user = db.UserProperty()
  
  # The user's nickname
  nickname = db.StringProperty(default='Anonymous')
  
  # The user's email
  email = db.EmailProperty()
  
  # The user's email
  ip = db.StringProperty(required=True)
  
  # The user's token to send msg via channel
  token = db.StringProperty()
  
  # timestamp is auto-updated when created
  created = db.DateTimeProperty(auto_now_add=True)
  
  @property
  def id(self):
    # This method just return it's key in str
    if self.is_saved():
      return str(self.key())
    else:
      return self.ip
  
  @property
  def is_anonymous(self):
    # This method return True if it is an anonymous player
    return not self.user
  
  @property
  def login_url(self):
    return users.create_login_url('/')
  
  @property
  def logout_url(self):
    return users.create_logout_url('/')
  
  @property
  def is_admin(self):
    return users.is_current_user_admin()
  
  
  
  
  
  ############################
  #  CACHING AND PERSISTING  #
  ############################
  
  
  persist = False
  persistent_attributes = ['user', 'nickname', 'email', 'token', 'status_ids']
  
  def __setattr__(self, name, value):
    if name in self.persistent_attributes:
      self.persist = True
    return object.__setattr__(self, name, value)
  
  def put(self, **kwargs):
    # NOW ANONYMOUS IS SAVED BY HIS IP
    self.add_message('player.put persist:'+str(self.persist)+
                     ' is_saved:'+str(self.is_saved()))
    # If it will be saved on datastore
    if self.persist or not self.is_saved():
      self.add_message('player.put on datastore')
      self.persist = False
      super(Player, self).put(**kwargs)
    
    # Anonymous is saved and gotted by its IPs
    if self.is_anonymous:
      memcache.set('anonymous'+self.ip, serialize(self))
    else:
      memcache.set('player'+self.user.user_id(), serialize(self))
  
  
  
  
  
  
  ###################
  #  PLAYER STATUS  #
  ###################
  
  
  # List playing status ids of this player
  status_ids = db.StringListProperty()
  
  # It retuns a list of all his status playing
  def get_status(self):
    # Returns a dict of serialized status saved in cache
    serialized_status = memcache.get_multi(self.status_ids,
                                           key_prefix='status')
    
    # Just copying my status_ids list to make some changes localy
    missing_status_ids = list(self.status_ids)
    player_status = []
    for status_id, status in serialized_status.iteritems():
      player_status.append(deserialize(status))
      missing_status_ids.remove(status_id)
    
    # Taking the missing status in database and add them in memcache
    if missing_status_ids:
      missing_status = Status.get(missing_status_ids)
      serialized_status = {}
      for status in missing_status:
        if status:
          serialized_status[status.id] = serialize(status)
          player_status.append(status)
      memcache.set_multi(serialized_status, key_prefix='status')
    
    return player_status
  
  
  def get_game_status(self, game):
    player_status = self.get_status()
    for status in player_status:
      if status.game.id == game.id:
        return status
    # If game not found in player_status
    return None
  
  
  
  
  
  
  
  #########################
  #  ENTER / LEAVE GAMES  #
  #########################
  
  
  def enter_game(self, game):
    game_status = self.get_game_status(game)
    
    if not game_status:
      query = Status.all()
      query.filter('game =', game)
      query.filter('player =', self)
      game_status = query.get()
      
      if not game_status:
        game_status = Status(player=self, game=game, playing=True)
        
    
    game_status.playing = True
    game_status.put()
    
    if game_status.id not in self.status_ids:
      self.status_ids.append(game_status.id)
      self.persist = True # It says that it should be saved in database
      self.put()
    
    # IT IS VERY WRONG, PLAYER SHOULD BE PUT IN A LIST,
    # AND THE LIST SHOULD BE ADDED TO GAME EACH create_match.
    game_status.game.add_status(game_status)
    
  
  
  def leave_game(self, game):
    game_status = self.get_game_status(game)
    
    if game_status:
      game_status.playing = False
      game_status.put()
      
      self.status_ids.remove(game_status.id)
      self.persist = True # It says that it should be saved in database
      self.put()
      
      # IT IS VERY WRONG, PLAYER SHOULD BE PUT IN A LIST TO LEAVE,
      # AND THE LIST SHOULD BE REMOVED TO GAME EACH create_match.
      game_status.game.remove_status(game_status)
  
  
  
  
  
  
  
  
  #####################
  #  PLAYER MESSAGES  #
  #####################
  
  
  def add_message(self, new_message):
    messages = memcache.get('messages'+self.id)
    if messages:
      messages.append(str(len(messages)+1)+': '+new_message)
      memcache.set('messages'+self.id, messages)
    else:
      memcache.set('messages'+self.id, ['1: '+new_message])
  
  def get_messages(self):
    messages = memcache.get('messages'+self.id)
    if messages:
      memcache.set('messages'+self.id, []) # Set a empty list
      return messages
    else:
      return []










#########################
#  AUXILIARY FUNCTIONS  #
#########################


# Get a current player and return it
# if player not logged in a google account, return a Anonymous player
def get_current_player(ip):
  user = users.get_current_user()
  if not user:
    player = get_current_anonymous(ip)
    player.add_message('Anonymous Player!')
    player.add_message('ip:'+str(player.ip))
    #memcache.set('anonymous'+player.ip, serialize(player))
    return player # Not logged, return a Anonymous player
  
  player = deserialize(memcache.get('player'+user.user_id()))
  
  if player:
    player.add_message('Player got on CACHE!')
    return player
  
  # Player not in cache, trying to get from datastore
  query = Player.all()
  query.filter('user =', user)
  player = query.get()
  if player:
    player.add_message('Player got in database!')
    #memcache.set('player'+player.user.user_id(), serialize(player))
    return player
  
  # Trying to get an anonymous player by this ip
  player = get_current_anonymous(ip)
  if player:
    player.user = user
    player.nickname = user.nickname()
    player.email = user.email()
    player.add_message('Player got by its Anonymous user (by ip)!')
    player.add_message('Now this player will not by anonymous anymore.')
    player.put()
    #memcache.set('player'+player.user.user_id(), serialize(player))
    memcache.delete('anonymous'+ip)
    return player
    
  # Do not exist in database yet
  player = Player(user = user,
                  nickname = user.nickname(),
                  email = user.email(),
                  ip = ip)
  player.add_message('NEW PLAYER!')
  player.put()
  #memcache.set('player'+player.user.user_id(), serialize(player))
  return player


# Get a current anonymous and return it based on his current ip
def get_current_anonymous(ip):
  #memcache.delete('anonymous'+ip)
  player = deserialize(memcache.get('anonymous'+ip))
  
  if player:
    player.add_message('Anonymous got on CACHE!')
    return player
  
  # Player not in cache
  query = Player.all()
  query.filter('ip =', ip)
  query.filter('user =', None)
  player = query.get()
  if player:
    player.add_message('Anonymous got in database!')
    player.put()
    return player
  
  # Do not exist in database yet
  # If he is anonymous will be saved just with his IP
  player = Player(ip = ip)
  player.add_message('NEW ANONYMOUS!')
  player.put()
  return player


