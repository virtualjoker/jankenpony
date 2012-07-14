# myapp.views.game
#
# Handler: Game
# It will creates a game, and handle matchs

import webapp2
import jinja2
import os

from google.appengine.api import users

from ..models.models import *



jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../templates/'))


class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      # Sux create fast solution
      #client = get_client(user=user, create=True)
      
      template_values = {
        'value1': 'Testing it',
        'value2': 'It is tested',
        }
      template = jinja_environment.get_template(
        'main.html')
      self.response.out.write(template.render(template_values))


class NotFoundHandler(webapp2.RequestHandler):
  def get(self):
    #self.response.out.write('Just testing Main')
    
    
    template_values = {
      'request_path': self.request.path,
      'request_url': self.request.url,
      }
    template = jinja_environment.get_template(
      'not_found.html')
    self.response.out.write(template.render(template_values))

