# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2
import jinja2
import os

from google.appengine.api import memcache
from aux import is_development
from aux import serialize_entities
from aux import deserialize_entities
from ..models.player import get_current_player
from ..models.game import Game

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../templates/'))


class MainHandler(webapp2.RequestHandler):
  def get(self):
    player = get_current_player()
    
    
    games = deserialize_entities(memcache.get('games'))
    if not games:
      query = Game.all()
      query.filter('active =', True)
      query.order('-online_players')
      games = query.fetch(limit=None)
      memcache.set('games', serialize_entities(games))
      return
    
    
    template_values = {
      'is_development': is_development,
      'player': player,
      'games': games,
      }
    
    template = jinja_environment.get_template('main.html')
    self.response.out.write(template.render(template_values))


