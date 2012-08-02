# myapp.models.status
#
# model: Status
# It store the status of a player in a game
# It indicates if player is playing or not, and its current balance

import json

from google.appengine.ext import db
from google.appengine.api import memcache
from ..aux import serialize
from ..aux import deserialize
from google.appengine.api.channel import send_message


shot_choices = ['nothing', 'rock', 'paper', 'scissors']

#
#  Ha uma inconsistencia com o cache de todas as referencias. CUIDADO!
#  A referencia do Game soh vai estar atualizada se puxada pelo
#  game.get_status, que faz o trabalho de atualizar sua propria referencia
#

class Status(db.Model):
  """ Status Model
      This model is used to save the progress
      did by one player in one game """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # Who enter in the queue? IT SHOULD BE A PLAYER
  player = db.ReferenceProperty(required=True,
                                collection_name='player_status_set')
  
  # What game this player will play?
  game = db.ReferenceProperty(required=True,
                                collection_name='game_status_set')
  
  # Playing, indicates if player is playing it now
  # Just player.enter_game/leave_game can handler this property
  playing = db.BooleanProperty(default=True)
  
  # This is the balance (saldo)
  # Wins - Losts, never less than zero
  balance = db.IntegerProperty(default=0)
  
  # timestamp is auto-updated when created
  # it indicates when this player entred in this queue
  created = db.DateTimeProperty(auto_now_add=True)
  
  
  
  
  
  
  
  
  
  ############################
  #  CACHING AND PERSISTING  #
  ############################
  
  
  persist = False
  persistent_attributes = ['balance', 'playing', 'match_counter']
  
  def __setattr__(self, name, value):
    if name in self.persistent_attributes:
      self.persist = True
    return object.__setattr__(self, name, value)
  
  # THIS PUT ISN'T ATUALIZING CACHE WITH THE CORRECT VALUES OF:
  # != SELF.PLAYER
  # != SELF.GAME
  def put(self, **kwargs):
    if self.persist or not self.is_saved():
      self.persist = False
      super(Status, self).put(**kwargs)
    #send_message(self.player.id, 'TESTING:'+str(self.persist))
    
    # HERE I'M SURE THAT I'M PUTTING IT ON CACHE WITH IN THE
    # VERY OLD PLAYER AND GAME VALUES
    memcache.set('status'+self.id, serialize(self))
  
  
  
  
  
  
  
  ###############
  #  GAME PLAY  #
  ###############
  
  challenger = db.SelfReferenceProperty(verbose_name='challenger_set')
  shots = db.StringListProperty(default=[])
  # For each match, increments it
  match_counter = db.IntegerProperty(default=0)
  wins = db.IntegerProperty(default=0)
  
  def shot(self, choice):
    # We will have game actualized every round, couse this status
    # will be take by game.get_status() who actualize the status.game
    if len(self.shots) < self.game.match_round:
      if choice in shot_choices:
        self.shots.append(choice)
        self.put()
        return True
    return False # If for some rason he cant shot
  
  
  def new_match(self, challenger):
    # Updating the challenger to a challanger of this match
    self.challenger = challenger
    
    # Is it realy necessary? We clear it when match ends in update_match
    #self.shots = []
    #self.challenger.shots = []
    
    self.send_match()
    
    self.put() # Make sure that it is saving just in cache !... ???
  
  def update_match(self, challenger):
    # Updating the challenger with its attualized shots
    self.challenger = challenger
    
    self.send_match()
    
    if self.game.match_round == 4: # When match ends...
      self.challenger = None
      self.shots = []
      self.wins = 0
      self.match_counter += 1 # It will force to save it in datastore
      self.persist = True # Forcing again, dunno why
    
    self.put() # Is it saving in cache when match_round != 3?

  
  def alone_match(self):
    self.balance += 1
    self.match_counter += 1
    self.challenger = None
    
    free_win = {}
    
    free_win['player'] = {
      'id':self.player.id,
      'nickname': self.player.nickname,
      'status': self.id,
      'shots': self.shots,
      'balance': self.balance,
      'match_counter': self.match_counter,
    }
    
    free_win['game'] = {
      'id': self.game.id,
      'name': self.game.name,
      'slug': self.game.slug,
      'players_counter': self.game.players_counter,
      'online_players': self.game.online_players,
      'match_counter': self.game.match_counter,
      'match_round': self.game.match_round,
      'datetime': self.game.last_match.strftime("%d/%m/%y %I:%M:%S %p"),
    }
    
    message = {'free_win': free_win}
    send_message(self.player.id, json.dumps(message))
    # When player do not play, it increments its match counter?
    # match_counter += 1
    self.put()
  
  
  def send_match(self):
    game_match = {}
    
    game_match['player'] = {
      'id':self.player.id,
      'nickname': self.player.nickname,
      'status': self.id,
      'shots': self.shots,
      'balance': self.balance,
      'match_counter': self.match_counter,
      'wins': self.wins,
    }
    
    game_match['challenger'] = {
      'id': self.challenger.player.id,
      'nickname': self.challenger.player.nickname,
      'status': self.challenger.id,
      'shots': self.challenger.shots,
      'balance': self.challenger.balance,
      'match_counter': self.challenger.match_counter,
      'wins': self.challenger.wins,
    }
    
    game_match['game'] = {
      'id': self.game.id,
      'name': self.game.name,
      'slug': self.game.slug,
      'players_counter': self.game.players_counter,
      'online_players': self.game.online_players,
      'match_counter': self.game.match_counter,
      'match_round': self.game.match_round,
      'datetime': self.game.last_match.strftime("%d/%m/%y %I:%M:%S %p"),
    }
    
    message = {'game_match': game_match}
    send_message(self.player.id, json.dumps(message))
  
  
  
  


  






#########################
#  AUXILIARY FUNCTIONS  #
#########################



# It returns a single status based on its id
def get_status(status_id):
  status = deserialize(memcache.get('status'+status_id))
  if status:
    return status
  
  status = Status.get(status_id)
  if not status: # If status not found
    return None
  
  memcache.set('status'+status.id, serialize(status))
  return status


