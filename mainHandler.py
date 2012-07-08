import webapp2


class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('This is my first out of JankenPony')

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug = True)
