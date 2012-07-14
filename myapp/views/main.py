# myapp.views.main
#
# Handler: Main
# It will create users, handler logins and logouts

import webapp2
import jinja2
import os
from datetime import datetime

from google.appengine.api import users

from ..models.player import Player

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../templates/'))


class Main(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    option = self.request.get('option', default_value=None)
    
    if option == 'create_game':
      pass
  
  def get(self):
    user = users.get_current_user()
    
    if not user:
      login_logout_url = users.create_login_url(self.request.uri)
      player = None
    else:
      login_logout_url = users.create_logout_url(self.request.uri)
      query = Player.all()
      query.filter('user =', user)
      player = query.get()
      if not player: # player == None
        player = Player(user = user,
                        nickname = user.nickname(),
                        email = user.email(), 
                        last_login = datetime.now())
        player.put()
      else: # This user has a player
        player.last_login == datetime.now()
        player.put()
    
    template_values = {
      'value1': 'Testing it',
      'value2': 'It is tested',
      'player': player,
      'login_logout_url': login_logout_url,
      }
    template = jinja_environment.get_template('main.html')
    self.response.out.write(template.render(template_values))


