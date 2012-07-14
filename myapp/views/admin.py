# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts
# DIFICULT: To transform the name of the game in a valid expression to URL
# so, I put the URL like input on the form to create a new game

import webapp2
import jinja2
import os

from ..models.player import get_current_player
from ..models.game import Game

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../templates/'))


class AdminHandler(webapp2.RequestHandler):
  def post(self):
    player = get_current_player()
    if not player.is_admin:
      template_values = {
        'player': player,
        }
      template = jinja_environment.get_template('restricted_access.html')
      self.response.out.write(template.render(template_values))
      return
    
    option = self.request.get('option', default_value=None)
    
    if option == 'create_game':
      name = self.request.get('name')
      game_id = self.request.get('game_id')
      active = bool(self.request.get('active'))
      # Check if exist a game with this link
      game = Game.all().filter('game_id =', game_id).get()
      if not game: # If doesn't exist, it will be saved
        game = Game(name=name, game_id=game_id, active=active)
        game.put()
    
    self.redirect('/admin')
  
  def get(self):
    player = get_current_player()
    if not player.is_admin:
      template_values = {
        'player': player,
        }
      template = jinja_environment.get_template('restricted_access.html')
      self.response.out.write(template.render(template_values))
      return
    
    
    query = Game.all()
    #query.filter('active =', True)
    query.order('created') # Order by created time in admins page
    games = query.fetch(limit=None)
    
    template_values = {
      'player': player,
      'games': games,
      }
    
    template = jinja_environment.get_template('admin.html')
    self.response.out.write(template.render(template_values))


