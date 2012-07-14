# myapp.models.match
#
# model: Math

from google.appengine.ext import db

from player import Player
from game import Game

shot_choices = set(["rock", "paper", "scissors"])

class Match(db.Model):
  """ Match Model
      This model will store the game's match """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # Who is the player1?
  player1 = db.ReferenceProperty(reference_class=Player, required=True, collection_name='player1_set')
  # The player1 shot
  player1_shot = db.StringProperty(choices=shot_choices, default=None)
  
  # Who is the player2?
  player2 = db.ReferenceProperty(reference_class=Player, required=True, collection_name='player2_set')
  # The player2 shot
  player2_shot = db.StringProperty(choices=shot_choices, default=None)
  
  # Who wins?
  winner = db.ReferenceProperty(reference_class=Player, default=None)
  
  # When become the Match ends
  finished = db.BooleanProperty(default=False)
  
  # Where this match comes from?
  game = db.ReferenceProperty(reference_class=Game, required=True)
  
  # Match number indicates whitch match it is
  # from the Game.match_counter
  number = db.IntegerProperty(required=True)
  
  # timestamp is auto-updated when created
  # it indicates when the player did the shot
  created = db.DateTimeProperty(auto_now_add=True)
  
  # the match timestamp
  match_datetime = db.DateTimeProperty()
