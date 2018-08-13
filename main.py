import webapp2
import os
import jinja2
from RecNation_models import Post, User
from content_management import populate_feed, logout_url, login_url
from google.appengine.ext import ndb
from google.appengine.api import users

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
        new_user_template = jinja_current_directory.get_template("templates/new_user.html")
        prev_user_template = jinja_current_directory.get_template("templates/prev_user.html")
        google_login_template = jinja_current_directory.get_template("templates/google_login.html")

        # get Google user
        user = users.get_current_user()

        if user:
            # look for user in datastore
            existing_user = User.query().filter(User.email == user.email()).get()
            nickname = user.nickname()
            if not existing_user:
                # prompt new users to sign up
                fields = {
                  "nickname": nickname,
                  "logout_url": logout_url,
                }
                self.response.write(new_user_template.render(fields))
            else:
                # direct existing user to feed
                self.redirect('/welcome')
        else:
            pass
            # Ask user to sign in to Google
            self.response.write(google_login_template.render({ "login_url": login_url }))

app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/welcome', WelcomeHandler),
], debug=True)
