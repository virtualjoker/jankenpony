import webapp2

from myapp.views.main import Main
#from myapp.views.game import Game

debug = True

url_map = [
            ('/', Main),
            #('/game', Game),
            #('/.*', NotFoundHandler)
          ]
app = webapp2.WSGIApplication(url_map, debug=debug)

