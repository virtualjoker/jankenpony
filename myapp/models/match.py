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

shot_choices = set(['nothing', 'rock', 'paper', 'scissors'])
match_round_choices = set([0, 1, 2, 3])

class Match(db.Model):
  """ Match Model
      This model will store the game's match """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # What is the player1 status?
  player1_status = db.ReferenceProperty(reference_class=Status, collection_name='player1_status_set')
  # The player1 shot
  player1_choices = db.ListProperty(item_type=str)
  
  # What is the player2 status?
  player2_status = db.ReferenceProperty(reference_class=Status, collection_name='player2_status_set')
  # The player2 shot
  player2_choices = db.ListProperty(item_type=str)
  
  # What round is playing right now?
  match_round = db.IntegerProperty(choices=match_round_choices, 
                                     default=0)
  # Store the datetime that process each round
  round_datetime = db.ListProperty(item_type=datetime)
  
  # Who wins?
  winner = db.ReferenceProperty(reference_class=Player, default=None, collection_name='match_winner_set')
  
  # Who loses?
  loser = db.ReferenceProperty(reference_class=Player, default=None, collection_name='match_loser_set')
  
  # When become the Match ends
  finished = db.BooleanProperty(default=False)
  
  # Where this match comes from?
  game = db.ReferenceProperty(reference_class=Game, required=True, collection_name='game_match_set')
  
  # Match number indicates whitch match it is
  # from the Game.match_counter
  number = db.IntegerProperty(required=True)
  
  # timestamp is auto-updated when created
  # it indicates when the player did the shot
  created = db.DateTimeProperty(auto_now_add=True)
  
  # HERE I HAVE TO REWRITE, CAUSE WE HAVE TO
  # ADD 3 SHOT TIMES TO EACH PLAYER
  # the match timestamp
  match_datetime = db.DateTimeProperty()





def set_game_matches(game_matches, game):
  # Here i will check how many time it is on cache,
  # If it is a lot of time, it should be saved on data
  memcache.set(game.id+'_matches', serialize(game_matches))


def get_game_matches(game):
  """ This function get games list
      and return it, if it is in cache or in data """
  
  game_matches = deserialize(memcache.get(game.id+'_matches'))
  if game_matches:
    return game_matches
  
  query = Match.all()
  query.filter('game =', game)
  query.filter('finished =', False)
  game_matches = query.fetch(limit=None)
  memcache.set(game.id+'_matches', serialize(game_matches))
  return game_matches

