# action.py
#
# Handler: ActionHandler

import webapp2
import json

from google.appengine.api.channel import create_channel
from google.appengine.ext.db import Key

from ..models.player import get_current_player
from ..models.game import Game
from ..models.match import Match

class ActionHandler(webapp2.RequestHandler):
  def post(self):
    player = get_current_player()
    
    # Action to execute
    action = self.request.get('action')
    
    # Arguments of the action
    args = self.request.get_all('args[]')
    
    # REMOVE ALL EMPTY VALUE OF THE ARGS (NOT IN USE FOR NOW)
    #for i in range(args.count('')):
    #  args.remove('')
    
    response = {}
    
    if action == 'get_token':
      # !!! IT IS CREATING A NEW CHANNEL EVERY TIME THAT
      # USER CHANGES THE PAGE, ITS DANGERS, JUST FOR NOW.
      player.token = create_channel(player.id)
      player.put()
      response['token'] = player.token
    
    if action == 'shot':
      #id = self.request.get('id')
      #response['id'] = json.dumps(args)
      match = Match.get(Key(args[0]))
      #response['player.nickname'] = player.nickname
      #response['player1.nickname'] = match.player1.nickname
      #response['player2.nickname'] = match.player2.nickname
      if player.id == match.player1.id:
        if not match.player1_choice:
          match.player1_choice = args[1]
          match.put()
          response['message'] = 'Chosed a '+match.player1_choice
        else:
          response['message'] = 'You already a '+match.player1_choice
      elif player.id == match.player2.id:
        if not match.player2_choice:
          match.player2_choice = args[1]
          match.put()
          response['message'] = 'Chosed a '+match.player2_choice
        else:
          response['message'] = 'You already a '+match.player2_choice
      
      
    
    self.response.out.write(json.dumps(response))


