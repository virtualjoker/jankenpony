# myapp.models.player
#
# model: Player

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from ..aux import serialize
from ..aux import deserialize

class Player(db.Model):
  """ Player Model
      This model will store players """
  
  # The Google's user account is required
  user = db.UserProperty()
  
  # The user's nickname
  nickname = db.StringProperty(default='Anonymous')
  
  # The user's email
  email = db.EmailProperty()
  
  # The user's token to send msg via channel
  token = db.StringProperty()
  
  # timestamp is auto-updated when created
  created = db.DateTimeProperty(auto_now_add=True)
  
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  @property
  def is_anonymous(self):
    # This method return True if it is an anonymous player
    # cause there is no Googles user account associated
    return not self.user
  
  @property
  def login_url(self):
    return users.create_login_url('/')
  
  @property
  def logout_url(self):
    return users.create_logout_url('/')
  
  @property
  def is_admin(self):
    return users.is_current_user_admin()



def get_current_player():
  """ This function get the player
      and return player and login_logout url """
  user = users.get_current_user()
  if not user:
    return Player() # Not logged, return empty player
  
  player = memcache.get(user.user_id())
  if player:
    return player
  
  # Player not in cache
  query = Player.all()
  query.filter('user =', user)
  player = query.get()
  if player:
    memcache.set(user.user_id(), player)
    return player
  
  # Do not exist in database yet
  player = Player(user = user,
                  nickname = user.nickname(),
                  email = user.email())
  player.put()
  memcache.set(user.user_id(), player)
  return player

