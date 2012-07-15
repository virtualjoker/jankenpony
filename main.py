import webapp2

from myapp.views.main import MainHandler
# Login depreceted to User area
#from myapp.views.login import LoginHandler
from myapp.views.admin import AdminHandler
from myapp.views.game import GameHandler
from myapp.views.server import ServerHandler
from myapp.views.action import ActionHandler

debug = True

url_map = [
            ('/', MainHandler),
            ('/admin', AdminHandler),
            (r'/game/(.*)', GameHandler),
            ('/server', ServerHandler),
            ('/action', ActionHandler),
            #('/.*', NotFoundHandler)
          ]
app = webapp2.WSGIApplication(url_map, debug=debug)
