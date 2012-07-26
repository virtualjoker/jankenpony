# action.py
#
# Handler: ActionHandler

import webapp2
import json

from google.appengine.api.channel import create_channel
from google.appengine.ext.db import Key

from ..models.player import get_current_player
from ..models.game import get_game_by_slug
#from ..models.game import Game
from ..models.match import Match

class ActionHandler(webapp2.RequestHandler):
  def get(self):
    self.post()
  def post(self):
    player = get_current_player(ip=self.request.remote_addr)
    
    # Action to execute
    action = self.request.get('action')
    
    # Arguments of the action
    args = self.request.get_all('args[]')
    
    # REMOVE ALL EMPTY VALUE OF THE ARGS (NOT NECESSARY YET)
    #for i in range(args.count('')):
    #  args.remove('')
    
    response = {
      'player': {
          'id': player.id,
          },
        'messages': [],
      }
    
    
    #############
    # GET TOKEN #
    #############
    
    if action == 'get_token':
      # It is called just if the clien't haven't the token yet,
      # or if the token failled on connection
      player.token = create_channel(player.id)
      response['token'] = player.token
    
    
    ########
    # SHOT #
    ########
    
    if action == 'shot':
      response['messages'].append('slug: '+args[0])
      response['messages'].append('player_choice: '+args[1])
      
      slug = args[0]
      game = get_game_by_slug(slug)
      if not game:
        response['messages'].append('NO GAME FOUND WITH THIS SLUG')
      else:
        player_status = player.get_game_status(game)
        choice = args[1]
        result = player_status.shot(choice)
        player_status.put()
        if result:
          response['messages'].append('You shot '+choice+' in '+
                                      str(game.match_round)+' round.')
        else:
          response['messages'].append('You didn\'t shot '+choice+'.')
          if len(player_status.shots) == player_status.game.match_round:
            response['messages'].append('You already shot in this match.')
      
    
    
    player.put()
    
    self.response.out.write(json.dumps(response))


