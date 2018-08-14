import webapp2
import os
import jinja2
import time
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
        user = users.get_current_user()
        if not user:
            self.redirect('/')
            return
        current_user = User.query().filter(User.email == user.email()).get()
        fields = {
            "username": current_user.username,
            "logout_url": logout_url,
            "email" : current_user.email
        }
        welcome_template = jinja_current_directory.get_template("templates/welcome.html")
        self.response.write(welcome_template.render(fields))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        current_user = User.query().filter(User.email == user.email()).get()
        if not current_user:
            new_user_entry = User(
                name = self.request.get("name"),
                username = self.request.get("username"),
                email = user.email(),
            )
            new_user_entry.put()
            current_user = new_user_entry
        else:
            new_post = Post(author= current_user.key, content= self.request.get("user_post"))
            new_post.put()
        time.sleep(.2)
        self.redirect('/welcome')

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        signup_template = jinja_current_directory.get_template(
            "templates/signup.html")
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.email()).get()
        fields = {
            "username": current_user.username,
            "logout_url": logout_url,
        }
        self.response.write(signup_template.render(fields))

class ForumHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        print("*********" + str(user) + "***********")
        if user is None:
            self.redirect('/')
            return # lol idk if this is ok?? it works I guess
        current_user = User.query().filter(User.email == user.email()).get()
        forum_fields = populate_feed(current_user)
        start_forum = jinja_current_directory.get_template("templates/forum.html")
        self.response.write(start_forum.render(forum_fields))

    def post(self):
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return # lol idk if this is ok?? it works I guess
        current_user = User.query().filter(User.email == user.email()).get()
        if not current_user:
            # upon new user form submission, create new user and store in datastore
            new_user_entry = User(
                name = self.request.get("name"),
                username = self.request.get("username"),
                email = user.email(),
            )
            new_user_entry.put()
            current_user = new_user_entry
        else:
            # if not a new user, existing user submitted a post from feed
            new_post = Post(author= current_user.key, content= self.request.get("user_post"))
            new_post.put()
        time.sleep(.2)
        self.redirect('/forum')

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
            # Ask user to sign in to Google
            self.response.write(google_login_template.render({ "login_url": login_url }))


app = webapp2.WSGIApplication([
    ('/', LoginHandler),
    ('/welcome', WelcomeHandler),
    ('/signup', SignUpHandler),
    ('/forum', ForumHandler),
], debug=True)
