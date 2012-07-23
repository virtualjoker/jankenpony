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
  def get(self):
    self.post()
  def post(self):
    player = get_current_player()
    
    # Action to execute
    action = self.request.get('action')
    
    # Arguments of the action
    args = self.request.get_all('args[]')
    
    # REMOVE ALL EMPTY VALUE OF THE ARGS (NOT IN USE FOR NOW)
    #for i in range(args.count('')):
    #  args.remove('')
    
    response = {
      'player': {
          'id': player.id,
          },
        'messages': [],
      }
    
    if action == 'get_token':
      # IT IS CREATING CHANNEL WHEN IT DOESN'T NEED
      player.token = create_channel(player.id)
      response['token'] = player.token
    
    if action == 'shot':
      # args[0] = game.id, args[1] = choice
      response['messages'].append('game.id:'+args[0])
      response['messages'].append('player1_status:'+args[1])
      response['messages'].append('player2_status:'+args[2])
      response['messages'].append('player_choice:'+args[3])
      query = Match.all()
      query.filter('game =', Key(args[0]))
      query.filter('player1_status =', Key(args[1]))
      query.filter('player2_status =', Key(args[2]))
      query.filter('finished =', False)
      match = query.get()
      
      # TESTING
      if not match:
        response['error'].append('No match found!')
        self.response.out.write(json.dumps(response))
        return
      
      
      # If this player is player1...
      if player.id == match.player1_status.player.id:
        player_choices = match.player1_choices
        response['messages'].append('You are player1 of this match')
      elif player.id == match.player2_status.player.id:
        player_choices = match.player2_choices
        response['messages'].append('You are player2 of this match')
      else:
        response['error'].append('Player not found in this match!')
        self.response.out.write(json.dumps(response))
        return
      
      response['messages'].append('Your choices '+str(match.player1_choices))
      
      # If this player haven't shot yet...
      # Every 13s the match will run and match round will be incremented
      if len(player_choices) == match.match_round:
        player_choices.append(args[3])
        match.put()
        response['messages'].append('You chose '+player_choices[len(player_choices)-1])
        response['chose'] = player_choices[len(player_choices)-1]
        
      else:
        response['messages'].append('You already a chose '+player_choices[len(player_choices)-1])
        response['chose'] = player_choices[len(player_choices)-1]
      
      
      response['messages'].append('Match round '+str(match.match_round))
    
    
    
    
    
    
    player.put()
    
    self.response.out.write(json.dumps(response))


