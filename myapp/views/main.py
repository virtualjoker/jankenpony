# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2

from ..aux import is_development
from ..aux import jinja_environment
from ..models.player import get_current_player
from ..models.player import Player
from ..models.game import get_games



class MainHandler(webapp2.RequestHandler):
  def get(self):
    player = get_current_player(ip=self.request.remote_addr)
    
    
    games = get_games()
    player.add_message('2PS: '+str(player.get_status()))
    
    template_values = {
      'is_development': is_development,
      'player': player,
      'games': games,
      'player_status': player.get_status(),
      'messages': player.get_messages(),
    }
    
    
    template = jinja_environment.get_template('main.html')
    self.response.out.write(template.render(template_values))


