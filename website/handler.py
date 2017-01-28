# Import the site
from website import site
from Model import User, Charity, CharityMember
from DBComm import DB

# Import flask objects
from flask import flash, session, redirect, render_template, url_for

# Import flask WTF Forms to handle login validation
from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, StringField, PasswordField
from wtforms.validators import Required

# Import the login objects
from flask.ext.login import UserMixin, login_required

@site.route('/', methods=['GET'])
<<<<<<< HEAD
def index():
    '''
    Home page
    '''
    return render_template('index.html', title='Home')

@site.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Handles active user log ins. Checks if
    user is already logged in.
    '''
    form = LoginForm()
    if form.validate_on_submit():
        print 'VALID LOGIN'
        flash(u'Successfully logged in as %s' % form.user.id)
        #session['user_id'] = form.user[0]
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@site.route("/signup", methods=["GET", 'POST'])
def sign_up():
    '''
    Handles new user sign ups
    '''
    form = SignupForm()
    if form.validate_on_submit():
        print 'Valid Sign up!'
        flash (u'Signed up successful!')
        #session['user_id'] = form.user[0]
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

class LoginForm(Form):
    '''
    Login class for validating user accounts by
    username and password.
    '''
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password',[validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        '''
        Initializer for login, no user is default.
        '''
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        '''
        Handles validating the user-password entered in.
        '''

        # Validate our form first
        rv = Form.validate(self)
        if not rv:
            return False

        # Now fetch the user
        user = User.get(self.username.data)

        if user is None:
            # No user found
            self.username.errors.append('Invalid login!')
            return False

        if not user.check_password(self.password.data):
            # Password invalid
            self.password.errors.append('Invalid login!')
            return False

        # Set the login form's user
        self.user = user
        return True

class SignupForm(Form):
    '''
    Signup form class for handling new user account validation.
    '''

    firstname = StringField('FirstName', [
        validators.DataRequired(),
        validators.Length(min=2)
    ])
    lastname = StringField('LastName')
    email = StringField('EmailAddress', [validators.Length(min=6, max=35)])

    username = StringField('Username', [
        validators.Length(min=2, max=35),
        validators.DataRequired()
    ])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match!')
    ])
    confirm = PasswordField('Repeat Password')

    def __init__(self, *args, **kwargs):
        '''
        Initializer for signup
        '''
        Form.__init__(self, *args, **kwargs)
        self.user = None


    def validate(self):
        '''
        Handles validating the sign up information
        '''

        # Validate our form first
        rv = Form.validate(self)
        if not rv:
            return False

        # TODO: Query to see if the email or username is already taken



class User(UserMixin):
    # proxy for a database of users
    user_database = {"luis": ("luis", "test"),
               "jenni": ("jenni", "test"),
               "tester": ("tester", "test")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    def check_password(self, password):
        '''
        Checks the password provided against the user account
        '''
        return (self.password == password)

    @classmethod
    def get(cls,id):
        # Query for the user account
        user_account = cls.user_database.get(id)

        # If the user account is valid, return it
        if user_account != None:
            return User(user_account[0], user_account[1])

        return None; # No account found
=======
@site.route('/helloWorld', methods=['GET'])
def Index():
    myDBObject = DB()



    myDBObject.connect()
    print "I'm connected!"

    #jenni_user = myDBObject.create_user("jenni2", "test", "jenni", "c", "jenni@gmail.com", "123456789")
    #print jenni_user

    #print myDBObject.get_user("j")
    print myDBObject.get_user(1)


    myDBObject.disconnect()
    print "I'm not connected!"

    #Hello, world test
    return "Hello, world! "


>>>>>>> 377de9a5da6fb1b9be8cb0ee7cb81600390cbcbd
