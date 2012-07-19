import webapp2

from myapp.views.main import MainHandler
# Login depreceted to User area
#from myapp.views.login import LoginHandler
from myapp.views.admin import AdminHandler
from myapp.views.game import GameHandler
from myapp.views.create_match import CreateMatchHandler
from myapp.views.run_match import RunMatchHandler
from myapp.views.action import ActionHandler

debug = True

url_map = [
            ('/', MainHandler),
            ('/admin', AdminHandler),
            (r'/game/(.*)', GameHandler),
            ('/create_match', CreateMatchHandler),
            ('/run_match', RunMatchHandler),
            ('/action', ActionHandler),
            #('/.*', NotFoundHandler)
          ]
app = webapp2.WSGIApplication(url_map, debug=debug)

