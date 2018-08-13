import webapp2
import os
import jinja2

jinja_current_directory = jinja2.Environment(
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

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login = jinja_current_directory.get_template("templates/login_screen.html")
        self.response.write(login.render())

app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/welcome', WelcomeHandler),
], debug=True)
