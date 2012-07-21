# myapp.models.game
#
# model: Game

from google.appengine.ext import db
from google.appengine.api import memcache
from ..aux import serialize
from ..aux import deserialize


class Game(db.Model):
  """ Game Model
      This model will store created games """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # The game's name
  name = db.StringProperty(required=True)
  
  # The game's link
  # It should be unique
  game_id = db.StringProperty(required=True)
  
  # It indicates when the game is active
  active = db.BooleanProperty(default=True)
  
  # It count how many players are played it all the time
  players_counter = db.IntegerProperty(default=0)
  
  # It count how many players are online in this game
  online_players = db.IntegerProperty(default=0)
  
  # Indicates the number of actual match, just a progressive counter
  # Every new match increments this number
  match_counter = db.IntegerProperty(default=0)
  
  # timestamp is auto-updated when created
  created = db.DateTimeProperty(auto_now_add=True)
  
  # timestamp of the last match
  last_match = db.DateTimeProperty()


def set_games(games):
  # Here i will check how many time it is on cache,
  # If it is a lot of time, it should be saved on data
  memcache.set('games', serialize(games))

def get_games():
  """ This function get games list
      and return it, if it is in cache or in data """
  
  games = deserialize(memcache.get('games'))
  if games:
    return games
  
  query = Game.all()
  query.filter('active =', True)
  games = query.fetch(limit=None)
  memcache.set('games', serialize(games))
  return games

