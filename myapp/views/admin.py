# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts
# DIFICULT: To transform the name of the game in a valid expression to URL
# so, I put the URL like input on the form to create a new game

import webapp2
import os

from google.appengine.ext import db
from ..aux import serialize
from ..aux import deserialize

from ..models.player import get_current_player
from ..models.game import Game
from ..models.game import get_game_by_slug
from ..aux import is_development
from ..aux import slugify
from ..aux import jinja_environment





class AdminHandler(webapp2.RequestHandler):
  def post(self):
    player = get_current_player(ip=self.request.remote_addr)
    # If this player isn't admin shows restricted_access page.
    if not player.is_admin:
      template_values = {
        'player': player,
        }
      template = jinja_environment.get_template('restricted_access.html')
      self.response.out.write(template.render(template_values))
      return
    
    option = self.request.get('option').lower()
    
    if option == 'create_game':
      name = self.request.get('name')
      slug = slugify(name)
      # Check if exist a game with this link
      game = get_game_by_slug(slug)
      if not game: # If doesn't exist, it will be saved
        game = Game(name=name, slug=slug)
        game.put()
        player.add_message('You created the game: '+ game.name)
      else:
        player.add_message('There is a game with this slug: '+ game.slug)
    
    if option == 'activate':
      game_id = self.request.get('game_id')
      game = db.get(game_id)
      game.start()
    
    if option == 'deactivate':
      game_id = self.request.get('game_id')
      game = db.get(game_id)
      # It will forces all players playing it to leave this game
      game.stop()
    
    # If option is to Deactive one game, this player should not be saved
    # couse if he was in the players playing this game, than he had
    # leave this game in cache and in database, but not in this session
    else:
      player.put()
    
    
    self.get()
    #self.redirect(self.request.uri)
  
  def get(self):
    player = get_current_player(ip=self.request.remote_addr)
    # If this player isn't admin shows restricted_access page.
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
      'is_development': is_development,
      'player': player,
      'games': games,
      'messages': player.get_messages(),
      }
    
    template = jinja_environment.get_template('admin.html')
    self.response.out.write(template.render(template_values))


