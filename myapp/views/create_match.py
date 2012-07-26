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
      
      # From 0 to len(game_status), just pair numbers
      # exclude for range the last item:
      # Last item will be a odd number (numero impar), or a single player
      for i in range(0, len(game_status)-1, 2):
        # I'm putting this players on this match! !!! \/ How?
        # I duuno how I'll be sure that the player is playing THIS match
        
        
        self.response.out.write(
          "---- Player1:"+game_status[i].player.nickname+' '+
          str(game_status[i].balance)+"<br />"+
          "---- Player2:"+game_status[i+1].player.nickname+' '+
          str(game_status[i+1].balance)+"<br />")
        
        # HERE WE NEED THEADS, CAUSE EACH NEW_MATCH WILL SEND A MESSAGE
        game_status[i].new_match(game_status[i+1])
        game_status[i+1].new_match(game_status[i])
        
        
        
      
      # Test if this game has a odd number of playing players
      if len(game_status)>0 and len(game_status)%2 == 1:
        # If there is odd number of playing players,
        # than the last one can't play cause he hasn't a pair this time
        game_status[len(game_status)-1].alone_match()
        self.response.out.write(
          "Alone player:"+
          str(game_status[len(game_status)-1].player.nickname)+' '+
          str(game_status[len(game_status)-1].balance)+"<br />")
      
      
      game.put()
    
    
    
    if self.request.headers.has_key("X-Appengine-Cron"):
      # Add the task to run matches in 11 secounds
      taskqueue.add(url='/run_match', method='GET', countdown='11')

