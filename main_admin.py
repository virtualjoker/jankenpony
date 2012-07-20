import webapp2

from myapp.views.create_match import CreateMatchHandler
from myapp.views.run_match import RunMatchHandler

debug = True

url_map = [
            ('/create_match', CreateMatchHandler),
            ('/run_match', RunMatchHandler),
          ]

app = webapp2.WSGIApplication(url_map, debug=debug)

