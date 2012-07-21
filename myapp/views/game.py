# myapp.views.game
#
# Handler: Game
# It will creates a game, and handle matchs

import webapp2
import jinja2
import os

from ..aux import is_development
from ..models.player import get_current_player
from ..models.game import Game
from ..models.status import Status
# Testing match
from ..models.match import Match

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../templates/'))


class GameHandler(webapp2.RequestHandler):
  def post(self, game_id):
    player = get_current_player()
    option = self.request.get('option')
    
    if not player.is_anonymous:
      query = Game.all()
      query.filter('active =', True)
      query.filter('game_id =', game_id)
      game = query.get()
      if game:
        query = Status.all()
        query.filter('player =', player)
        query.filter('game =', game)
        status = query.get()
        
        if option == 'sign_up':
          if not status:
            status = Status(player=player, game=game)
            status.put()
            game.online_players += 1
            game.put()
        
        elif option == 'sign_in':
          if status:
            if status.playing == False:
              status.playing = True
              status.put()
              game.online_players += 1
              game.put()
        
        elif option == 'sign_out':
          if status:
            if status.playing == True:
              status.playing = False
              status.put()
              game.online_players -= 1
              game.put()
    
    self.redirect(self.request.uri)
  
  def get(self, game_id):
    player = get_current_player()
    
    
    query = Game.all()
    query.filter('active =', True)
    query.filter('game_id =', game_id)
    game = query.get()
    
    status = None
    if not player.is_anonymous:
      query = Status.all()
      query.filter('player =', player)
      query.filter('game =', game)
      status = query.get()
    
    query = Status.all()
    query.filter('game =', game)
    query.filter('playing =', True)
    status_list = query.fetch(limit=None)
    
    query = Match.all()
    query.filter('game =', game)
    query.filter('finished =', False)
    matchs = query.fetch(limit=None)
    
    template_values = {
      'is_development': is_development,
      'player': player,
      'game': game,
      'status': status,
      'status_list': status_list,
      'matchs': matchs,
      }
    template = jinja_environment.get_template('game.html')
    self.response.out.write(template.render(template_values))


