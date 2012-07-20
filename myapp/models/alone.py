# myapp.models.alone
#
# model: Alone

from google.appengine.ext import db

from player import Player
from status import Status
from game import Game

class Alone(db.Model):
  """ Alone Model
      This model will store the player who can't play
      the actual match, cause it has a odd playing players
      and he can't play it alone """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # What is the alone player status?
  player_status = db.ReferenceProperty(reference_class=Status)
  
  # Where this match comes from?
  game = db.ReferenceProperty(reference_class=Game, required=True)
  
  # Match number indicates whitch match it is
  # from the Game.match_counter
  match_number = db.IntegerProperty(required=True)
  
  # timestamp is auto-updated when created
  created = db.DateTimeProperty(auto_now_add=True)

