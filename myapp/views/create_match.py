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
from google.appengine.api import taskqueue
#from google.appengine.ext import deferred
from google.appengine.ext import db
from google.appengine.api import memcache

from ..aux import serialize
from ..aux import deserialize
from ..models.game import get_games
from ..models.game import set_games
from ..models.status import get_game_status
from ..models.status import set_game_status
from ..models.match import get_game_matches
from ..models.match import set_game_matches
from ..models.match import Match

def send(token1, token2, message):
  send_message(token1, message)
  send_message(token2, message)


class CreateMatchHandler(webapp2.RequestHandler):
  def get(self):
    
    self.response.out.write("Server test<br />")
    
    
    
    games = get_games()
    
    
    for game in games:
      game.match_counter += 1
      game.last_match = datetime.now()
      
      game_matches = []
      
      self.response.out.write(
        "Creating matches #"+str(game.match_counter)+
        " for game: "+game.name+"<br />")
      
      
      game_status = get_game_status(game)
      
      
      self.response.out.write(
        "Len of players playing:"+str(len(game_status))+"<br />")
      self.response.out.write(
        "Range:"+str(range(0, len(game_status)-1, 2))+"<br />")
      
      # From 0 to len(game_status), just pair numbers
      # exclude for range the last item:
      # Last item will be a odd number (numero impar), or a single player
      for i in range(0, len(game_status)-1, 2):
        
        match = Match(player1_status=game_status[i],
                      player2_status=game_status[i+1],
                      game=game,
                      number=game.match_counter,
                      match_round=0)
        
        self.response.out.write(
          "---- Player1:"+game_status[i].player.nickname+"<br />"+
          "---- Player2:"+game_status[i+1].player.nickname+"<br />")
        
        
        game_matches.append(match)
        
        match_dic = {
          'player1': match.player1_status.player.id,
          'player1_status': match.player1_status.id,
          'player2': match.player2_status.player.id,
          'player2_status': match.player2_status.id,
          'game': match.game.id,
          'number': match.number,
          'match_round': match.match_round,
        }
        message = json.dumps({'game_match': match_dic})
        
        # FOR NOW IT IS NO PROBLEM
        #deferred.defer(send, player1.id, player2.id, message)
        send(match.player1_status.player.id,
             match.player2_status.player.id,
             message)
        
        
      
      # Test if this game has a odd number of playing players
      if len(game_status)%2 == 1:
        # If there is odd number of playing players,
        # than the last one can't play cause he hasn't a pair this time
        message = {'alerts': ['You will not play this time, cause you is the last of an odd list.']}
        send_message(game_status[len(game_status)-1].player.id, message)
        self.response.out.write(
          "Alone player:"+game_status[len(game_status)-1].player.nickname+"<br />")
      
      # Continue the for game in games
      set_game_status(game_status, game)
      set_game_matches(game_matches, game)
      for match in game_matches:
        self.response.out.write(
          "match p1:"+str(match.player1_status.player.nickname)+"<br />")
        self.response.out.write(
          "match p2:"+str(match.player2_status.player.nickname)+"<br />")
    
    
    set_games(games)
    
    if self.request.headers.has_key("X-Appengine-Cron"):
      # Add the task to run matches in 11 secounds
      taskqueue.add(url='/run_match', method='GET', countdown='11')

