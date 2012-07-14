# myapp.models.queue
#
# model: Queue
# Players will have a position on queue, this position will
# be calculated by a Query orded by 'created' with match = None

from google.appengine.ext import db

from player import Player
from game import Game

class Queue(db.Model):
  """ Queue Model
      This model will store when a player is in a game queue """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # Who enter in the queue?
  player = db.ReferenceProperty(reference_class=Player, required=True)
  
  # What game this player will play?
  game = db.ReferenceProperty(reference_class=Game, required=True)
  
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
