# myapp.views.create_match
#
# Handler: CreateMatchHandler
# It will create pairs and create matches

import webapp2
import json
from datetime import datetime
from random import shuffle

from google.appengine.api import taskqueue
from ..models.game import get_games


class CreateMatchHandler(webapp2.RequestHandler):
  def get(self):
    
    self.response.out.write("Server test<br />")
    
    
    games = get_games()
    if not games:
      self.response.out.write("Just there is no games<br />")
      return
    
    for game in games:
      game.match_counter += 1
      # Starting NOW the first round of this match
      game.match_round = 1
      game.last_match = datetime.now()
      
      
      self.response.out.write(
        "Creating matches #"+str(game.match_counter)+
        " for game: "+game.name+
        " id: "+game.id+"<br />")
      
      
      game_status = game.get_status()
      
      # Randomize this list of status to change the pair every match
      shuffle(game_status)
      
      self.response.out.write("GS:"+str(game_status)+"<br />")
      if len(game_status) > 0:
        self.response.out.write("GS2:"+str(game_status[0].game.id)+"<br />")
      
      
      self.response.out.write(
        "Len of players playing:"+str(len(game_status))+"<br />")
      self.response.out.write(
        "Range:"+str(range(0, len(game_status)-1, 2))+"<br />")
      
      # While there is 2 or more palyers in the list
      while len(game_status)>=2:
       
        player_status = game_status.pop()
        challenger_status = game_status.pop()
      
        self.response.out.write(
          "---- Player: "+player_status.player.nickname+' '+
          str(player_status.balance)+"<br />"+
          "---- Challenger: "+challenger_status.player.nickname+' '+
          str(challenger_status.balance)+"<br />")
        
        # HERE WE NEED THEADS, CAUSE EACH NEW_MATCH WILL SEND A MESSAGE
        player_status.new_match(challenger_status)
        challenger_status.new_match(player_status)
        
        
        
        
      # Test if this game has a odd number of playing players,
      # then, here we've just 1 player left
      if len(game_status)>0:
        alone_status = game_status.pop()
        alone_status.alone_match()
        self.response.out.write(
          "Alone player: "+
          str(alone_status.player.nickname)+' '+
          str(alone_status.balance)+"<br />")
      
      
      game.put()
    
    
    
    if self.request.headers.has_key("X-Appengine-Cron"):
      # Add the task to run matches in 11 secounds
      taskqueue.add(url='/run_match', method='GET', countdown='11')

