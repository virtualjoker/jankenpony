# myapp.models.status
#
# model: Status
# It store the status of a player in a game
# It indicates if player is playing or not, and its current balance

from google.appengine.ext import db
from google.appengine.api import memcache
from ..aux import serialize
from ..aux import deserialize

from player import Player
from game import Game

class Status(db.Model):
  """ Status Model
      This is it """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # Who enter in the queue?
  player = db.ReferenceProperty(reference_class=Player, required=True)
  
  # What game this player will play?
  game = db.ReferenceProperty(reference_class=Game, required=True)
  
  # Playing, indicates if player is playing it now
  playing = db.BooleanProperty(default=True)
  
  # This is the balance (saldo)
  # Wins - Losts, never less than zero
  balance = db.IntegerProperty(default=0)
  
  # How many matches this player played in this game?
  match_counter = db.IntegerProperty(default=0)
  
  # timestamp is auto-updated when created
  # it indicates when this player entred in this queue
  created = db.DateTimeProperty(auto_now_add=True)
  
  # Last match time
  last_match = db.DateTimeProperty(auto_now_add=True)



def set_game_status(game_status, game):
  # Here i will check how many time it is on cache,
  # If it is a lot of time, it should be saved on data
  memcache.set(game.id+'_status', serialize(game_status))


def get_game_status(game):
  """ This function get games list
      and return it, if it is in cache or in data """
  
  game_status = deserialize(memcache.get(game.id+'_status'))
  if game_status:
    return game_status
  
  query = Status.all()
  query.filter('game =', game)
  query.filter('playing =', True)
  query.order('-balance') # Order by (win-loses)
  game_status = query.fetch(limit=None)
  memcache.set(game.id+'_status', serialize(game_status))
  return game_status
