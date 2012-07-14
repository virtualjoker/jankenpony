# myapp.views.login
#
# Handler: Login
# Path: /login
# When user logs in to a Googles account, he will be
# redirected to here, and here we will check if he has a Player
# If he hasn't a player, we create it
# If he has a player, we update last_login datetime
# DEPRECETED TO /USER HANDLER

import webapp2
from datetime import datetime

from google.appengine.api import users

from ..models.player import Player

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    
    if user: # If it is logged in to a Googles account
      query = Player.all()
      query.filter('user =', user)
      player = query.get()
      if not player: # player == None, do not exist in database yet
        player = Player(user = user,
                        nickname = user.nickname(),
                        email = user.email(), 
                        last_login = datetime.now())
        player.put()
      else: # This user has a player
        player.last_login == datetime.now()
        player.put()
    
    self.redirect("/")


