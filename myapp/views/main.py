# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2
import jinja2
import os

from google.appengine.api import memcache
from ..aux import is_development
from ..aux import serialize
from ..aux import deserialize
from ..models.player import get_current_player
from ..models.game import get_games

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../templates/'))


class MainHandler(webapp2.RequestHandler):
  def get(self):
    player = get_current_player()
    
    games = get_games()
    
    
    template_values = {
      'is_development': is_development,
      'player': player,
      'games': games,
      }
    
    template = jinja_environment.get_template('main.html')
    self.response.out.write(template.render(template_values))


