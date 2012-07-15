import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



class MainHandler(webapp2.RequestHandler):
  def get(self):
    #self.response.out.write('Just testing Main')
    
    
    template_values = {
      'request_path': self.request.path,
      'request_url': self.request.url,
      }
    template = jinja_environment.get_template(
      'template/not_found.html')
    self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([(r'/.*', MainHandler)],
                              debug=True)

# comment
