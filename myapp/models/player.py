# myapp.models.player
#
# model: Player

from google.appengine.ext import db

class Player(db.Model):
  """ Player Model
      This model will store players """
      
  @property
  def id(self):
    # This method just return it's key in str
    return str(self.key())
  
  # The Google's user account is required
  user = db.UserProperty(required=True)
  
  # The user's nickname
  nickname = db.StringProperty(required=True)
  
  # The user's email
  email = db.StringProperty(required=True)
  
  # timestamp is auto-updated when created
  created = db.DateTimeProperty(auto_now_add=True)
  
  # timestamp of last login
  last_login = db.DateTimeProperty()
