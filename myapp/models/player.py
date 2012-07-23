# myapp.models.player
#
# model: Player

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from status import Status
from ..aux import serialize
from ..aux import deserialize

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
  
  # The user's token to send msg via channel
  token = db.StringProperty()
  
  # timestamp is auto-updated when created
  created = db.DateTimeProperty(auto_now_add=True)
  
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
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
    if not self.is_anonymous:
      self.add_message('Player save persist:'+str(self.persist))
      if self.persist or not self.is_saved():
        self.persist = False
        super(Player, self).put(**kwargs)
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
        game_status.put()
    
    game_status.playing = True
    memcache.set('status'+game_status.id, serialize(game_status))
    
    if game_status.id not in self.status_ids:
      self.status_ids.append(game_status.id)
      self.persist = True # It says that it should be saved in database
      self.put()
    
    game_status.game.add_status(game_status)
    
  
  
  def leave_game(self, game):
    game_status = self.get_game_status(game)
    
    if game_status:
      game_status.playing = False
      game_status.put()
      memcache.delete('status'+game_status.id)
      
      self.status_ids.remove(game_status.id)
      self.persist = True # It says that it should be saved in database
      self.put()
      
      game_status.game.remove_status(game_status)
  
  
  
  
  
  
  
  
  #####################
  #  PLAYER MESSAGES  #
  #####################
  
  # List of messages, saved just in cache
  messages = db.StringListProperty()
  
  def add_message(self, messages):
    self.messages.append(messages)
  
  def get_messages(self):
    msgs = self.messages
    self.messages = []
    return msgs










#########################
#  AUXILIARY FUNCTIONS  #
#########################

# Get a current player and return it
# if player not logged in a google account, return a Anonymous player
def get_current_player():
  user = users.get_current_user()
  if not user:
    return Player() # Not logged, return a Anonymous player
  
  player = deserialize(memcache.get('player'+user.user_id()))
  
  if player:
    player.add_message('Player got on CACHE!')
    return player
  
  # Player not in cache
  query = Player.all()
  query.filter('user =', user)
  player = query.get()
  if player:
    player.put()
    return player
  
  # Do not exist in database yet
  player = Player(user = user,
                  nickname = user.nickname(),
                  email = user.email())
  player.put()
  return player

