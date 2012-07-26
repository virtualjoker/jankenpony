# myapp.views.game
#
# Handler: GameHandler
# ...

import webapp2
import os

from ..aux import is_development
from ..aux import jinja_environment
from ..models.player import get_current_player
from ..models.game import get_game_by_slug


class GameHandler(webapp2.RequestHandler):
  def post(self, slug):
    player = get_current_player(ip=self.request.remote_addr)
    option = self.request.get('option')
    
    if not player.is_anonymous:
      game = get_game_by_slug(slug)
      if game:
        if option == 'enter':
          player.enter_game(game)
        elif option == 'leave':
          player.leave_game(game)
    #player.nickname='testing'
    #player.put()
    self.redirect(self.request.uri)
  
  
  
  def get(self, slug):
    player = get_current_player(ip=self.request.remote_addr)
    
    game = get_game_by_slug(slug)
    
    #self.response.out.write('Game:'+str(game)+'<br/>')
    #return
    if game:
      game_status = game.get_status()
      player_status = player.get_game_status(game)
    else:
      game_status = None
      player_status = None
    
    player.add_message('GS:'+str(game_status))
    
    template_values = {
      'is_development': is_development,
      'player': player,
      'game': game,
      'slug': slug,
      'player_status': player_status,
      'game_status': game_status,
      'messages': player.get_messages(),
      }
    
    player.put()
    template = jinja_environment.get_template('game.html')
    self.response.out.write(template.render(template_values))


