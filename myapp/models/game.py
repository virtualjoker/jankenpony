# myapp.models.game
#
# model: Game

from google.appengine.ext import db


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
