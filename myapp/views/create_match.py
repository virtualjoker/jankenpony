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

from aux import serialize_entities
from ..models.game import Game
from ..models.status import Status
from ..models.match import Match
from ..models.alone import Alone

def send(token1, token2, message):
  send_message(token1, message)
  send_message(token2, message)


class CreateMatchHandler(webapp2.RequestHandler):
  def get(self):
    
    self.response.out.write("Server test<br />")
    
    # To create a new match we have be right that
    # there is no unfinished match
    # For this run_match must to play 3 times
    # If for some rason run_match didn't run 3 times,
    # we force to finish the matches
    query = Match.all()
    query.filter('finished =', False)
    matches = query.fetch(limit=None)
    for match in matches:
      match.finished = True
    db.put(matches)
    
    
    query = Game.all()
    query.filter('active =', True)
    query.order('-online_players')
    games = query.fetch(limit=None)
    matches = []
    all_alone = []
    
    for game in games:
      game.match_counter += 1
      game.match_datetime = datetime.now()
      
      self.response.out.write(
        "Creating matches #"+str(game.match_counter)+
        " for game: "+game.name+"<br />")
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
                      number=game.match_counter,
                      match_round=0)
        
        self.response.out.write(
          "---- Player1:"+status_list[i].player.nickname+"<br />"+
          "---- Player2:"+status_list[i+1].player.nickname+"<br />")
        
        matches.append(match)
        
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
      if len(status_list)%2 == 1:
        # If there is odd number of playing players,
        # than the last one can't play cause he hasn't a pair this time
        alone = Alone(player_status=status_list[len(status_list)-1],
                      game=game,
                      match_number=game.match_counter)
        all_alone.append(alone)
        self.response.out.write(
          "Alone player:"+status_list[len(status_list)-1].player.nickname+"<br />")
        break # This player will not play this time
      
      
    
    #memcache.set('games', serialize_entities(games))
    db.put(games)
    db.put(matches)
    db.put(all_alone)
    
    if self.request.headers.has_key("X-Appengine-Cron"):
      # Add the task to run matches in 11 secounds
      taskqueue.add(url='/run_match', method='GET', countdown='11')

