import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



class MainHandler(webapp2.RequestHandler):
  def get(self):
    #self.response.out.write('Just testing Main')
    
    
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

