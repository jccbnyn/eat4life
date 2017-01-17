# Import the site and login manager of this module
from website import site, login_manager

# Import flask objects
from flask import render_template

# Import the login objects
from flask.ext.login import UserMixin, login_required

@site.route('/', methods=['GET'])
@site.route('/helloWorld', methods=['GET'])
def Index():
    return render_template('index.html',
            title='Home')

@site.route('/login', methods=['GET'])
def Login():
    return render_template('login.html',
            title='Login')

@site.route("/protected/",methods=["GET"])
@login_required
def protected():
    return 'Hello, Protected World!'

class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
               "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None
