# myapp.models.match
#
# model: Math

from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import memcache
from ..aux import serialize
from ..aux import deserialize

from player import Player
from status import Status
from game import Game


class Match(db.Model):
  """ Match Model
      This model will store the game's match """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  
  # What is this match round?
  # Just a copy of game.match_counter at the time of this match creation.
  match_round = db.IntegerProperty()
  
  # Store the datetime that process each round
  round_datetime = db.ListProperty(item_type=datetime)
  
  # Where this match comes from?
  game = db.ReferenceProperty(reference_class=Game, required=True, collection_name='game_match_set')
  
  # timestamp is auto-updated when created
  # it indicates when the player did the shot
  created = db.DateTimeProperty(auto_now_add=True)
  
  # HERE I HAVE TO REWRITE, CAUSE WE HAVE TO
  # ADD 3 SHOT TIMES TO EACH PLAYER
  # the match timestamp
  match_datetime = db.DateTimeProperty()



