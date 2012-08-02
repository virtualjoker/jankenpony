# myapp.views.run_match
#
# Handler: RunMatchHandler
# It will runs current not finished matches

import webapp2
import json
from datetime import datetime
import os

from google.appengine.api import memcache
from google.appengine.api.channel import send_message
from google.appengine.api import taskqueue
from google.appengine.ext import deferred
from google.appengine.ext import db

# It will be used to access player propertyes in one player_status.player.id
from ..models.player import Player



from ..models.game import get_games



# !!! REMEMBER TO LOGOUT USERS THAT DIDN'T ANY CHOSE (AFK USERS)
class RunMatchHandler(webapp2.RequestHandler):
  def get(self):
    
    #for name in os.environ.keys():
    #  self.response.out.write("%s = %s<br />\n" % (name, os.environ[name]))
    
    
    games = get_games()
    
    if not games:
      self.response.out.write("Just there is no games<br />")
      return
    
    # This variable means if it needs a new round to finish
    run_new_round = False
    for game in games:
      # Here match_round indicates the next round
      game.match_round += 1
      # When match_round == 4 it will calcule the results of 3rd round
      if game.match_round > 4:
        self.response.out.write("This game finished<br />")
        continue
      elif game.match_round < 4:
        run_new_round = True
      
      
      # It returns a dict of all status playing this match of this game
      game_status_dict = game.get_status_dict()
      
      if not game_status_dict:
        self.response.out.write("This game has no player playing<br />")
        continue
      
      
      
      while len(game_status_dict):
        
        # Get the next status to handle
        player_status_id, player_status = game_status_dict.popitem()
        
        # Check if this player is in match, cause he can be the alone
        # or he can be a new player in this game
        if not player_status.challenger:
          self.response.out.write("The haven't a challenger<br />")
          continue
        
        # If challenger isn't in the list, its an erro
        if player_status.challenger.id not in game_status_dict:
          self.response.out.write("The challenger isn't in the list<br />")
          continue
        
        # If the challenger is in the list...
        challenger_status = game_status_dict.pop(player_status.challenger.id)
        
        # If player didn't shot this round
        # match_round - 1 cause it will indicates the next round
        if len(player_status.shots) < game.match_round - 1 :
          self.response.out.write("This player didn't shot this match<br />")
          player_status.shot('nothing')
        
        
        # If challenger didn't shot this round
        if len(challenger_status.shots) < game.match_round - 1 :
          self.response.out.write("The challenger didn't play this match<br />")
          challenger_status.shot('nothing')
        
        
        self.response.out.write(
          "m.p:"+str(player_status.shots)+"<br />"+
          "m.c:"+str(challenger_status.shots)+"<br />")
        
        self.response.out.write('TESTE<br>')
        
        # Check who wins this round, and increments status.wins
        judge(game.match_round, player_status, challenger_status)
        
        
        # Check the match winner and give his point
        if game.match_round == 4:
          if player_status.wins > challenger_status.wins:
            player_status.balance += 1
            challenger_status.balance -= 1
            if challenger_status.balance < 0:
              challenger_status.balance = 0
          elif player_status.wins < challenger_status.wins:
            challenger_status.balance += 1
            player_status.balance -= 1
            if player_status.balance < 0:
              player_status.balance = 0
        
        
        
        
        
        self.response.out.write(
          "wins.p:"+str(player_status.wins)+"<br />"+
          "wins.c:"+str(challenger_status.wins)+"<br />")
        
        
        
        
        
        
        
        
        
        
        self.response.out.write('TESTE<br>')
        
        player_status.update_match(challenger_status)
        challenger_status.update_match(player_status)
      
      
      # Continue in 'for game in games:'
      game.put()
    
    # Check if it needs a new round to end this match
    if run_new_round:
      # If it was auto-call by task queue, than it needs to recall itself
      if self.request.headers.has_key("X-AppEngine-QueueName"):
        taskqueue.add(url='/run_match', method='GET', countdown='11')















def judge(match_round, player_status, challenger_status):
  # Actual shot [i]
  i = match_round - 2
  if player_status.shots[i] == challenger_status.shots[i]:
    pass # They played the same, noone wins
  elif player_status.shots[i] == 'nothing' and \
       challenger_status.shots[i] != 'nothing':
    challenger_status.wins += 1 # Player didn't shot, challenger wins
  elif challenger_status.shots[i] == 'nothing' and \
       player_status.shots[i] != 'nothing':
    player_status.wins += 1 # Challenger didn't shot, player wins
  elif player_status.shots[i] == 'rock':
    if challenger_status.shots[i] == 'papper':
      challenger_status.wins += 1
    elif challenger_status.shots[i] == 'scissors':
      player_status.wins += 1
  elif player_status.shots[i] == 'papper':
    if challenger_status.shots[i] == 'rock':
      player_status.wins += 1
    elif challenger_status.shots[i] == 'scissors':
      challenger_status.wins += 1
  elif player_status.shots[i] == 'scissors':
    if challenger_status.shots[i] == 'rock':
      challenger_status.wins += 1
    elif challenger_status.shots[i] == 'papper':
      player_status.wins += 1





