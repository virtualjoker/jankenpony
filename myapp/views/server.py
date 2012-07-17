# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2
import datetime
import json
from time import time

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


class ServerHandler(webapp2.RequestHandler):
  def get(self):
    # Remember to change, first build a set of changes of entitys,
    # than just do one put with all the changes, its better.
    
    self.response.out.write("FIRST TEST<br/>")
    
    # Gives the win if challenger didn't play and
    # cencelling all the not played by both
    query = Match.all()
    query.filter('finished =', False)
    matchs = query.fetch(limit=None)
    status_list = []
    for match in matchs:
      self.response.out.write(
        "m.p1:"+str(match.player1_choice)+"<br />"+
        "m.p2:"+str(match.player2_choice)+"<br />")
      match.finished = True
      # Lets chose the winner
      # If noone shot it, it has no winner
      if not match.player1_choice and not match.player2_choice:
        self.response.out.write("DEBUGGING<br />")
        pass # pass or continue, just nothing to add in winner
      # If just player1 didn't shot, player 2 wins
      elif not match.player1_choice: 
        match.winner = match.player2
      # If just player2 didn't shot, player 1 wins
      elif not match.player2_choice: 
        match.winner = match.player1
      # If both shotted, lets see who wins
      else:
        # If both shotted same option, it has no winner
        if match.player1_choice == match.player2_choice:
          pass # pass or continue, just nothing to add in winner
        elif match.player1_choice == 'rock' and match.player2_choice == 'paper':
          match.winner = match.player2
        elif match.player1_choice == 'rock' and match.player2_choice == 'scissors':
          match.winner = match.player1
        elif match.player1_choice == 'paper' and match.player2_choice == 'rock':
          match.winner = match.player1
        elif match.player1_choice == 'paper' and match.player2_choice == 'scissors':
          match.winner = match.player2
        elif match.player1_choice == 'scissors' and match.player2_choice == 'rock':
          match.winner = match.player2
        elif match.player1_choice == 'scissors' and match.player2_choice == 'paper':
          match.winner = match.player1
          
      
      
      # Changing the player status
      if not match.winner:
        match.player1_status.balance -= 1
        match.player2_status.balance -= 1
      else:
        if match.winner == match.player1:
          match.player1_status.balance += 1
          match.player2_status.balance -= 1
        else:
          match.player1_status.balance -= 1
          match.player2_status.balance += 1
      
      # Match can't be less than 0
      if match.player1_status.balance < 0:
        match.player1_status.balance = 0
      if match.player2_status.balance < 0:
        match.player2_status.balance = 0
      
      status_list.append(match.player1_status)
      status_list.append(match.player2_status)
      
      # Just to see who wins it:
      if not match.winner:
        self.response.out.write("Match draws<br />")
      else:
        self.response.out.write("Winner:"+match.winner.nickname+"<br />")
      self.response.out.write("p1_status.balance:"+str(match.player1_status.balance)+"<br />")
      self.response.out.write("p2_status.balance:"+str(match.player2_status.balance)+"<br />")
    
    db.put(status_list)
    db.put(matchs)
    
    
    
    query = Game.all()
    query.filter('active =', True)
    query.filter('online_players >', 1)
    query.order('-online_players')
    games = query.fetch(limit=None)
    
    
    self.response.out.write("Server test<br />")
    
    for game in games:
      
      
      self.response.out.write("Game:"+game.name+"<br />")
      query = Status.all()
      query.filter('game =', game)
      query.filter('playing =', True)
      query.order('-balance') # Order by (win-loses)
      status_list = query.fetch(limit=None)
      
      self.response.out.write("-- Status list:<br />")
      
      player1, player2 = None, None
      for status in status_list:
        if not player1:
          player1 = status.player
          player1_status = status
        else:
          player2 = status.player
          player2_status = status
          match = Match(player1=player1,
                        player1_status=player1_status,
                        player2=player2,
                        player2_status=player2_status,
                        game=game,
                        number=game.match_counter)
          self.response.out.write(
            "---- Player1:"+player1.nickname+"<br />"+
            "---- Player2:"+player2.nickname+"<br />")
          match.put()
          
          # Just to check delay time
          t0 = time()
          match_dic = {
            'player1': player1.id,
            'player2': player2.id,
            'game': match.game.id,
            'number': match.number,
            'id': match.id,
          }
          message = json.dumps({'new_match': match_dic})
          
          # FOR NOW IT IS NO PROBLEM
          #deferred.defer(send, player1.id, player2.id, message)
          send(player1.id, player2.id, message)
          
          delay = time() - t0
          self.response.out.write("Delay:"+str(delay)+"<br />")
          
          player1, player2 = None, None
      
      message = json.dumps({
        'message': 'You are alone, and you not play this time!'
        })
      
      if player1 and not player2:
        deferred.defer(send_message, player1.id, message)
      
      game.match_counter += 1
      game.match_datetime = datetime.datetime.now()
      game.put()
      
      
    
    


