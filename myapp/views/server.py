# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2
import datetime
import json
from time import time

from google.appengine.api.channel import send_message
from google.appengine.ext import deferred

from ..models.game import Game
from ..models.status import Status
from ..models.match import Match

def send(token, message):#, handlerSelf):
  
  send_message(token, message)
  #handlerSelf.response.out.write("MSG sent:"+message+"<br>")
  #handlerSelf.response.out.write("Token:"+player.token+"<br />")


class ServerHandler(webapp2.RequestHandler):
  def get(self):
    # Remember to change, first build a set of changes of entitys,
    # than just do one put with all the changes, its better.
    
    query = Game.all()
    query.filter('active =', True)
    query.filter('online_players >', 1)
    query.order('-online_players')
    games = query.fetch(limit=None)
    
    
    self.response.out.write("Server test<br />")
    
    for game in games:
      # Gives the win if challenger didn't play and
      # cencelling all the not played by both
      query = Match.all()
      query.filter('finished =', False)
      matchs = query.fetch(limit=None)
      for match in matchs:
        self.response.out.write(
          "m.p1:"+str(match.player1_shot)+"<br />"+
          "m.p2:"+str(match.player2_shot)+"<br />")
        if not match.player1_shot and not match.player2_shot:
          self.response.out.write("finish<br/>")
          match.finished = True
          match.put()
        # Here I have checked if p1 and p2 didn't shot, but I have to
        # check if one of them shotted and the challenger didn't
        #elif not player1.shot: 
          #match
      
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
        else:
          player2 = status.player
          match = Match(player1=player1,
                        player2=player2,
                        game=game,
                        number=game.match_counter)
          self.response.out.write(
            "---- Player1:"+player1.nickname+"<br />"+
            "---- Player2:"+player2.nickname+"<br />")
          match.put()
          
          # Just to check delay time
          t0 = time()
          match_dic = {
            'player1': match.player1.id,
            'player2': match.player2.id,
            'game': match.game.id,
            'number': match.number,
          }
          message = json.dumps({'match': match_dic})
          # STARTIN THE HIPER TEST
          for i in range(50):
            deferred.defer(send, player1.id, message)
            deferred.defer(send, player2.id, message)
          
          delay = time() - t0
          self.response.out.write("Delay:"+str(delay)+"<br />")
          
          player1, player2 = None, None
      
      game.match_counter += 1
      game.match_datetime = datetime.datetime.now()
      game.put()
      
      
    
    


