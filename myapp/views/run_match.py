# myapp.views.run_match
#
# Handler: RunMatchHandler
# It will runs current not finished matches

import webapp2
import json
from datetime import datetime
import os
from aux import is_development

from google.appengine.api import memcache
from google.appengine.api.channel import send_message
from google.appengine.ext import deferred
from google.appengine.ext import db

from ..models.game import Game
from ..models.status import Status
from ..models.match import Match

def send(token1, token2, message):
  send_message(token1, message)
  send_message(token2, message)


# !!! REMEMBER TO LOGOUT USERS THAT DIDN'T ANY CHOSE (AFK USERS)
class RunMatchHandler(webapp2.RequestHandler):
  def get(self):
    # Remember to change, first build a set of changes of entitys,
    # than just do one put with all the changes, its better.
    
    #for name in os.environ.keys():
    #  self.response.out.write("%s = %s<br />\n" % (name, os.environ[name]))
    #self.response.out.write("xxDEVELOPMENT == " + str(is_development)+"<br>")
    
    query = Match.all()
    query.filter('finished =', False)
    matches = query.fetch(limit=None)
    status_list = []
    for match in matches:
      # If it is the first round, match_round is default value 0,
      # then we increments to know that will be the first round
      match.match_round += 1
      
      self.response.out.write(
        "match_round:"+str(match.match_round)+"<br />")
      
      match.round_datetime.append(datetime.now())
      
      # If player1 didn't shot this round
      if len(match.player1_choices) < match.match_round:
        self.response.out.write("P1 didn't shot this round<br />")
        match.player1_choices.append('nothing')
      
      # If player2 didn't shot this round
      if len(match.player2_choices) < match.match_round:
        self.response.out.write("P2 didn't shot this round<br />")
        match.player2_choices.append('nothing')
      
      
      self.response.out.write(
        "m.p1:"+str(match.player1_choices)+"<br />"+
        "m.p2:"+str(match.player2_choices)+"<br />")
      
      
      # CHOSING THE WINNER IN ROUND 3
      if match.match_round == 3:
        match.finished = True # If it is the last round, it finishes here.
        
        player1_wins = 0
        player2_wins = 0
        for i in range(3):
          
          if match.player1_choices[i] == match.player2_choices[i]:
            continue # If they play the same choice it draws and noone wins
          
          elif match.player1_choices[i] == 'nothing':
            player2_wins +=1 # Remember p2 didn't shot the same choice
          
          elif match.player2_choices[i] == 'nothing':
            player1_wins +=1 # Remember p1 didn't shot the same choice
             
          elif match.player1_choices[i] == 'stone':
            if match.player2_choices[i] == 'paper':
              player2_wins +=1
            elif match.player2_choices[i] == 'scissors':
              player1_wins +=1
          
          elif match.player1_choices[i] == 'paper':
            if match.player2_choices[i] == 'rock':
              player1_wins +=1
            elif match.player2_choices[i] == 'scissors':
              player2_wins +=1
          
          elif match.player1_choices[i] == 'scissors':
            if match.player2_choices[i] == 'rock':
              player2_wins +=1
            elif match.player2_choices[i] == 'paper':
              player1_wins +=1
        
        # If player 1 wins
        if player1_wins > player2_wins:
          match.winner = match.player1_status.player
          match.loser = match.player2_status.player
          match.player1_status.balance += 1
          # Never status.balance will be less than 0
          if match.player2_status.balance > 0:
            match.player2_status.balance -= 1
          status_list.append(match.player1_status)
          status_list.append(match.player2_status)
        
        # If player 2 wins
        elif player1_wins < player2_wins:
          match.loser = match.player1_status.player
          match.winner = match.player2_status.player
          match.player2_status.balance += 1
          # Never status.balance will be less than 0
          if match.player1_status.balance > 0:
            match.player1_status.balance -= 1
          status_list.append(match.player1_status)
          status_list.append(match.player2_status)
      
      # Endif round == 3 (just to remmeber)
      # All the match rounds we have to send message to players
      match_dic = {
        'player1': match.player1_status.player.id,
        'player1_status': match.player1_status.id,
        'player2': match.player2_status.player.id,
        'player1_choices': match.player1_choices,
        'player2_status': match.player2_status.id,
        'player2_choices': match.player2_choices,
        'game': match.game.id,
        'number': match.number,
        'match_round': match.match_round,
      }
      
      # If it is the last round, there is a winner and a loser, or draws
      if match.match_round == 3:
        if (match.winner):
          match_dic['winner'] = match.winner.id
        if (match.loser):
          match_dic['loser'] = match.loser.id
      
      self.response.out.write("MSG"+str(match_dic)+"<br />")
      message = json.dumps({'game_match': match_dic})
      # FOR NOW IT IS NO PROBLEM
      #deferred.defer(send, player1.id, player2.id, message)
      send(match.player1_status.player.id,
           match.player2_status.player.id,
           message)
    
    db.put(status_list)
    db.put(matches)
    
    
      
      
    
    


