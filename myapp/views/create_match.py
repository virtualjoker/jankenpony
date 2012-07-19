# myapp.views.create_match
#
# Handler: CreateMatchHandler
# It will create pairs and create matches

import webapp2
import json
from datetime import datetime
#from time import time

#from google.appengine.api import memcache
from google.appengine.api.channel import send_message
from google.appengine.ext import deferred
from google.appengine.ext import db

from ..models.game import Game
from ..models.status import Status
from ..models.match import Match

def send(token1, token2, message):
  send_message(token1, message)
  send_message(token2, message)


class CreateMatchHandler(webapp2.RequestHandler):
  def get(self):
    
    self.response.out.write("Server test<br />")
    
    
    query = Game.all()
    query.filter('active =', True)
    games = query.fetch(limit=None)
    matches = []
    alone = []
    
    for game in games:
      game.match_counter += 1
      game.match_datetime = datetime.now()
      
      self.response.out.write(
        "Creating matches for game:"+game.name+"<br />")
      query = Status.all()
      query.filter('game =', game)
      query.filter('playing =', True)
      query.order('-balance') # Order by (win-loses)
      status_list = query.fetch(limit=None)
      
      self.response.out.write(
        "Len of players playing:"+str(len(status_list))+"<br />")
      self.response.out.write(
        "Range:"+str(range(0, len(status_list)-1, 2))+"<br />")
      # From 0 to len(status_list), just pair numbers
      # exclude for range the last item:
      # Last item will be a odd number (numero impar), or a single player
      for i in range(0, len(status_list)-1, 2):
        
        match = Match(player1_status=status_list[i],
                      player2_status=status_list[i+1],
                      game=game,
                      number=game.match_counter)
        
        self.response.out.write(
          "---- Player1:"+status_list[i].player.nickname+"<br />"+
          "---- Player2:"+status_list[i+1].player.nickname+"<br />")
        
        matches.append(match)
        
        match_dic = {
          'player1': match.player1_status.player.id,
          'player2': match.player2_status.player.id,
          'game': match.game.id,
          'number': match.number,
          # We can't send ID cause it wasn't create yed
          #'id': match.id,
        }
        message = json.dumps({'new_match': match_dic})
        
        # FOR NOW IT IS NO PROBLEM
        #deferred.defer(send, player1.id, player2.id, message)
        send(match.player1_status.player.id,
             match.player2_status.player.id,
             message)
        
        # Increments the counter, cause we took the next player
        # to make pair with actual player
        i += 1
      
      # Test if this game has a odd number of playing players
      if len(status_list)%2 == 1:
        # 
        alone.append(status_list[len(status_list)])
        self.response.out.write(
          "Alone player:"+status_list[i].player.nickname+"<br />")
        break # This player will not play this time
    
    
    db.put(games)
    db.put(matches)

