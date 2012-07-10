import webapp2
import jinja2
import os

from google.appengine.api import users

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



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
        'template/main.html')
      self.response.out.write(template.render(template_values))



app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/index.html', MainHandler)],
                              debug=True)

