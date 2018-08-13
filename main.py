import webapp2
import os
import jinja2

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#class MainHandler(webapp2.RequestHandler):
    #def get(self):
        #self.response.write("Welcome to Recreation Nation")

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = jinja_current_directory.get_template(
            "templates/welcome.html")
        self.response.write(welcome_template.render())

app = webapp2.WSGIApplication([
    ('/welcome', WelcomeHandler),
], debug=True)
