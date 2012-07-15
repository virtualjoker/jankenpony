# action.py
#
# Handler: ActionHandler

import webapp2
import json

from google.appengine.api.channel import create_channel

from ..models.player import get_current_player
from ..models.game import Game

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
      
    
    self.response.out.write(json.dumps(response))


