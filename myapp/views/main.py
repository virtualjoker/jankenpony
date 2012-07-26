# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2
import os

from ..aux import is_development
from ..aux import jinja_environment
from ..models.player import *
from ..models.game import *



class MainHandler(webapp2.RequestHandler):
  def get(self):
    player = get_current_player(ip=self.request.remote_addr)
    
    
    games = get_games()
    #self.response.out.write('Game:'+str(games)+'<br/>')
    #return
    #player.add_message('PS_ids: '+str(player.status_ids))
    player.add_message('PS: '+str(player.get_status()))
    
    template_values = {
      'is_development': is_development,
      'player': player,
      'player_status': player.get_status(),
      'games': games,
      'messages': player.get_messages(),
    }
    
    #self.response.out.write(str(template_values))
    player.put()
    template = jinja_environment.get_template('main.html')
    self.response.out.write(template.render(template_values))


