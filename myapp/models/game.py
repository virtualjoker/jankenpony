# myapp.models.game
#
# model: Game

from google.appengine.ext import db
from google.appengine.api import memcache
from ..aux import serialize
from ..aux import deserialize
from status import Status


class Game(db.Model):
  """ Game Model
      This model show the game properties and
      the methods to manipulate his properties """
  
  #######################
  #  PUBLIC PROPERTIES  #
  #######################
  
  
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # The game's name
  name = db.StringProperty(required=True)
  
  # The game's link
  # It should be unique
  slug = db.StringProperty(required=True)
  
  # It indicates when the game is active
  # should not be acessed directly, use start() and stop() methods
  active = db.BooleanProperty(default=False)
  
  # timestamp is auto-updated when created
  created = db.DateTimeProperty(auto_now_add=True)
  
  # It count how many players played it all the time
  players_counter = db.IntegerProperty(default=0)
  
  # It count how many players are online in this game
  online_players = db.IntegerProperty(default=0)
  
  # Indicates the number of actual match, just a progressive counter
  # Every new match increments this number
  match_counter = db.IntegerProperty(default=0)
  
  # Indicates what round is the actual match 0='not in match'
  match_round = db.IntegerProperty(default=0)
  
  
  # timestamp of the last match
  last_match = db.DateTimeProperty(auto_now_add=True)
  
  
  
  
  
  
  
  ############################
  #  CACHING AND PERSISTING  #
  ############################
  
  def put(self, **kwargs):
    super(Game, self).put(**kwargs)
    # Games doesn't have any reference to any entity, for that when we
    # are saving it we can save it in memcache too, cause there is no
    # entity desactualized in there
    if self.active:
      memcache.set('game'+self.slug, serialize(self))
    else:
      memcache.delete('game')
  
  
  
  
  
  #######################
  #  START / STOP GAME  #
  #######################
  
  def start(self):
    self.active = True
    game_slugs = get_game_slugs() # Get a list of game slugs in cache
    
    if self.slug not in game_slugs:
      game_slugs.append(self.slug)
      memcache.set('game_slugs', game_slugs)
    
    self.put() # It will store in DB and Cache cause .active was changed
  
  def stop(self):
    self.active = False
    game_slugs = get_game_slugs()
    
    if self.slug in game_slugs:
      game_slugs.remove(self.slug)
      memcache.set('game_slugs', game_slugs)
    
    
    serialized_status = memcache.get_multi(self.status_ids,
                                           key_prefix='status')
    
    # Just copying my status_ids list to make some changes localy
    missing_status_ids = list(self.status_ids)
    for status_id, status in serialized_status.iteritems():
      deserialized_status = deserialize(status)
      deserialized_status.player.leave_game(self)
      missing_status_ids.remove(status_id)
    
    # Taking the missing status in database
    if missing_status_ids:
      missing_status = Status.get(missing_status_ids)
      for status in missing_status:
        status.player.leave_game(self)
    
    memcache.delete('game'+self.slug)
    self.status_ids = []
    self.put()
  
  
  
  
  
  
  #################
  #  GAME STATUS  #
  #################
  
  
  # List playing status ids for this game
  status_ids = db.StringListProperty()
  
  def actualise_status(self, game_status):
    # Actualizing the game saved on each status cached
    # We are sure that using this funciton status.game are atualized
    if type(game_status) == type([]):
      for status in game_status:
        status.game = self
    elif type(game_status) == type({}):
      for status_id, status in game_status.iteritems():
        status.game = self
  
  
  
  # It retuns a list of all status playing this game
  def get_status(self, write=None):
    # It will returns a serialized status in mem_cache
    serialized_status = memcache.get_multi(self.status_ids,
                                                key_prefix='status')
    # Just copying my status_ids list to make some changes localy
    missing_status_ids = list(self.status_ids)
    game_status = []
    for status_id, status in serialized_status.iteritems():
      game_status.append(deserialize(status))
      missing_status_ids.remove(status_id)
    
    # Taking the missing status in database and add them in memcache
    if missing_status_ids:
      missing_status = Status.get(missing_status_ids)
      serialized_status = {}
      for status in missing_status:
        serialized_status[status.id] = serialize(status)
        game_status.append(status)
      memcache.set_multi(serialized_status, key_prefix='status')
    
    # I really dunno why, but the game_status list in this function
    # works like a list of string, and when this function pass to some
    # function or when it returns, game_status assume its really identity
    # that is a list of status, not a list of strings... (crazy, I know)
    self.actualise_status(game_status)
    
    return game_status # Returns a random list of Status playing this game
  
  
  
  
  
  # It retuns a DICT of all status playing this game
  def get_status_dict(self, write=None):
    # It will returns a serialized status in mem_cache
    serialized_status = memcache.get_multi(self.status_ids,
                                                key_prefix='status')
    # Just copying my status_ids list to make some changes localy
    missing_status_ids = list(self.status_ids)
    game_status = {}
    for status_id, status in serialized_status.iteritems():
      game_status[status_id] = deserialize(status)
      missing_status_ids.remove(status_id)
    
    # Taking the missing status in database and add them in memcache
    if missing_status_ids:
      missing_status = Status.get(missing_status_ids)
      serialized_status = {}
      for status in missing_status:
        game_status[status_id] = deserialize(status)
        serialized_status[status.id] = serialize(status)
        
      memcache.set_multi(serialized_status, key_prefix='status')
    
    # I really dunno why, but the game_status list in this function
    # works like a list of string, and when this function pass to some
    # function or when it returns, game_status assume its really identity
    # that is a list of status, not a list of strings... (crazy, I know)
    self.actualise_status(game_status)
    
    return game_status # Returns a random list of Status playing this game
  
  
  
  
  
  
  #########################
  #  ADD / REMOVE STATUS  #
  #########################
  
  # It will be auto called by player when he enters a game
  def add_status(self, status):
    if status.id not in self.status_ids:
      self.status_ids.append(status.id)
      self.persist = True # It says that it should be saved in database
      self.put()
  
  
  # It will be auto scalled by player when he leaves a game
  def remove_status(self, status):
    if status.id in self.status_ids:
      self.status_ids.remove(status.id)
      self.persist = True # It says that it should be saved in database
      self.put()














#########################
#  AUXILIARY FUNCTIONS  #
#########################

# Get the slugs list of active games
def get_game_slugs():
  game_slugs = memcache.get('game_slugs')
  if game_slugs:
    return game_slugs
  
  query = Game.all()
  query.filter('active =', True)
  games = query.fetch(limit=None)
  
  game_slugs = []
  for game in games:
    game_slugs.append(game.slug)
  
  memcache.set('game_slugs', game_slugs)
  return game_slugs


# It returns a single active game based in its slug
def get_game_by_slug(slug):
  game = deserialize(memcache.get('game'+slug))
  if game:
    return game
  
  query = Game.all()
  query.filter('active =', True)
  query.filter('slug =', slug)
  game = query.get()
  if not game: # If game not found or it is unactive
    return None
  
  memcache.set('game'+game.slug, serialize(game))
  return game


# It returns a list of active games
def get_games():
  game_slugs = get_game_slugs()
  if game_slugs:
    serialized_games = memcache.get_multi(game_slugs, key_prefix='game')
    
    # Checking game in slug and not in cache
    missing_slugs = list(game_slugs)
    games = []
    if serialized_games:
      for slug, game in serialized_games.iteritems():
        games.append(deserialize(game))
        missing_slugs.remove(slug)
    
    if missing_slugs:
      query = Game.all()
      query.filter('active =', True)
      query.filter('slug in', missing_slugs)
      missing_games = query.fetch(limit=None)
      serialized_games = {}
      for game in missing_games:
        games.append(game)
        serialized_games[game.slug] = serialize(game)
      memcache.set_multi(serialized_games, key_prefix='game')
    
    return games





##############################################################
'''
### DEPRECATED
def set_games(games, return_game_slugs=False): # It saves a list of games
  
  # Atualizing the game_slugs list and every game caches
  game_slugs = []
  games_by_slug = {}
  for game in games:
    game_slugs.append(game.slug)
    games_by_slug[game.slug] = serialize(game)
  
  memcache.set('game_slugs', game_slugs)
  # HERE WE HAVE TO SAVE WHAT IS IN CACHE FIRST
  memcache.set_multi(games_by_slug, key_prefix='game_by_slug')
  
  if return_game_slugs:
    return game_slugs
'''




