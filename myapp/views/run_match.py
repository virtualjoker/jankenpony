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

# It will be used to access player propertyes in one status.player.id
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
      else:
        # It needs a new round to finish this match
        run_new_round = True
      
      
      # It returns a dict of all status playing this match of this game
      game_status_dict = game.get_status_dict()
      
      if not game_status_dict:
        self.response.out.write("This game has no player playing<br />")
        continue
      
      
      
      while len(game_status_dict):
        
        # Get the next status to handle
        status_id, status = game_status_dict.popitem()
        
        # If challenger isn't in the list, there is nothing to do (ERROR HERE)
        if status.challenger.id not in game_status_dict:
          self.response.out.write("The challenger isn't in the list<br />")
          continue
        # If the challenger is in the list...
        challenger = game_status_dict.pop(status.challenger.id)
        
        # If player didn't shot this round
        # match_round - 1 cause it will indicates the next round
        if len(status.shots) < game.match_round - 1 :
          self.response.out.write("This player didn't shot this match<br />")
          status.shot('nothing')
        
        
        # If challenger didn't shot this round
        if len(challenger.shots) < game.match_round - 1 :
          self.response.out.write("The challenger didn't play this match<br />")
          challenger.shot('nothing')
        
        
        self.response.out.write(
          "m.p:"+str(status.shots)+"<br />"+
          "m.c:"+str(challenger.shots)+"<br />")
        
        status.update_match(challenger)
        challenger.update_match(status)
      
      
      # Continue in 'for game in games:'
      game.put()
    
    # Check if it needs a new round to end this match
    if run_new_round:
      # If it was auto-call by task queue, than it needs to recall itself
      if self.request.headers.has_key("X-AppEngine-QueueName"):
        taskqueue.add(url='/run_match', method='GET', countdown='11')



