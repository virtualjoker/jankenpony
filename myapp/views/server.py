# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2
import datetime

from ..models.game import Game
from ..models.status import Status
from ..models.match import Match



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
          player1, player2 = None, None
      
      game.match_counter += 1
      game.match_datetime = datetime.datetime.now()
      game.put()
      
      
    
    


