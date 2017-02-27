# Import the site
from website import site, mail, login_manager

# Import DB objects
from Model import User, Charity, CharityMember
from DBComm import DB

# Import flask objects
from flask import abort, current_app, flash, \
        session, redirect, render_template, url_for

# Import WTForms to handle form templates
from flask.ext.wtf import Form

# Import WTForms helpers
from wtforms import validators
from wtforms.fields import DateField, DateTimeField, HiddenField, TextField, \
       SelectField, SelectMultipleField, StringField, PasswordField

from wtforms.validators import Required, StopValidation
from wtforms import widgets

from flask.ext.login import UserMixin, current_user, login_required, \
        login_user, logout_user

# Import ItsDangerous for crypyo signing IDs
from itsdangerous import URLSafeSerializer, BadSignature

# Import datetime object
from datetime import datetime

@site.route('/account', methods=['GET'])
@login_required
def account_home():
    '''
    The user account's home page
    '''
    return render_template('account_home.html')

@site.route('/account/details', methods=['GET', 'POST'])
@login_required
def account_details():
    '''
    Account details page. Allows user to update information.
    '''

    form = EditAccountForm()
    form.populate_fields(current_user)

    if form.validate_on_submit():
        current_app.logger.debug("New user sign up for user %s"
                % form.user.userName)

        flash (u'Sign up successful!'
                + 'Please check your email to complete sign up process')

        # Now send an email with the verification link
        serializer = URLSafeSerializer(site.secret_key)
        url = serializer.dumps(form.user.userID)

        mail.sendMail(form.user.emailAddress,
                'Eat4Life - Verification Required',
                'Please verify your email: http://localhost:5000/activate/'
                + url)

        current_app.logger.debug("Sent email for new user sign up to %s"
                % form.user.emailAddress)

        return redirect(url_for('index'))

    flash_errors(form)
    return render_template('account_details.html', form=form)

@site.route('/account/host-a-dinner', methods=['GET', 'POST'])
@login_required
def hostdinner():
    '''
    Handles host a dinner page
    '''
    form = HostEventForm()
    if form.validate_on_submit():
        # TODO: Add a nice flash message, detailing the event & time
        flash(u'Successfully hosted a dinner for in as %s'
                % form.event.eventDate)
        # TODO: Add a landing page for hosted events
        return redirect(url_for('hosted-events'))

    flash_errors(form)
    return render_template('host-a-dinner.html', form=form)

@site.route('/', methods=['GET'])
def index():
    '''
    Home page
    '''
    if current_user != None:
        if current_user.is_authenticated:
            return redirect(url_for('account_home'))

    return render_template('index.html', title='Home')

@site.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Handles active user log ins. Checks if
    user is already logged in.
    '''

    form = LoginForm()
    if form.validate_on_submit():
        current_app.logger.debug("Valid login as user %s"
                % form.user.userName)
        flash(u'Successfully logged in as %s' % form.user.userName)
        login_user(form.user)
        return redirect(url_for('account_home'))

    flash_errors(form)
    return render_template('login.html', form=form)

@site.route('/logout', methods=['GET'])
@login_required
def logout():
    '''
    Handles logging out the active user
    '''
    current_app.logger.debug("Logging out as user %s"
            % current_user.userName)
    logout_user()
    flash(u'Successfully logged out')
    return redirect(url_for('index'))

@site.route("/signup", methods=["GET", 'POST'])
def sign_up():
    '''
    Handles new user sign ups
    '''

    form = SignupForm()
    if form.validate_on_submit():
        current_app.logger.debug("New user sign up for user %s"
                % form.user.userName)

        flash (u'Sign up successful!'
                + 'Please check your email to complete sign up process')

        # Now send an email with the verification link
        serializer = URLSafeSerializer(site.secret_key)
        url = serializer.dumps(form.user.userID)

        mail.sendMail(form.user.emailAddress,
                'Eat4Life - Verification Required',
                'Please verify your email: http://localhost:5000/activate/'
                + url)

        current_app.logger.debug("Sent email for new user sign up to %s"
                % form.user.emailAddress)

        return redirect(url_for('index'))

    flash_errors(form)
    return render_template('signup.html', form=form)

@site.route("/mail", methods=['GET'])
def mail_test():
    '''
    Sends a test email
    '''
    # TODO: Removes this in prod
    #mail.sendMail('luis111290@gmail.com', 'Hello!', 'Test Message!')
    return "Sent"

@site.route("/activate/<key>", methods=['GET'])
def activate_user(key):
    '''
    Handles verifying that the user's email account is valid.
    '''
    # Create a serializer using our app's secret key
    serializer = URLSafeSerializer(site.secret_key)
    # Try to load in the key to verify it
    try:
        user_id = serializer.loads(key)
    except BadSignature:
        abort(404)

    # Fetch the user based on the decrypted user ID
    db = DB()
    db.connect()
    # Valid user, update/verify account
    # TODO: Notify user account is valid now, redirect to account screen
    db.verify_user_by_id(user_id)
    db.disconnect()

    return 'Successful!'

@site.route('/genkey/<user_id>', methods=['GET'])
def generate_key(user_id):
    '''
    THIS IS ONLY FOR TESTING. DON'T USE IN PROD
    '''
    # TODO: Remove this once tested that serialization works
    serializer = URLSafeSerializer(site.secret_key)
    url = serializer.dumps(user_id)
    return url

def flash_errors(form):
    '''
    Function expects a Flask WTF Form and will
    flash the error messages in the HTML form.
    '''
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                u"Error in the %s field - %s"
                % (getattr(form, field).label.text,error))

@login_manager.user_loader
def user_loader(user_id):
    """
    Function needs to be defined for the LoginManager.
    Function expects a user ID, returns a User class object.
    """
    db = DB()
    return db.get_user_by_id(user_id)

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class HostEventForm(Form):
    '''
    Host event form class for validating a host event data
    '''

    event_date = DateField(
        "Event Date", format="%m/%d/%Y",
        validators=[validators.DataRequired()])

    event_time = DateTimeField(
        "Event Time", format="%I:%M%p",
        validators=[validators.DataRequired()])

    event_location_address = StringField('Address', [
        validators.DataRequired(),
        validators.Length(min=2, max=35,
            message="Address must be 2-35 characters long.")])

    event_location_city = TextField('City', [
        validators.DataRequired(),
        validators.Length(
            min=2, max=35,
            message="City must be 2-35 characters long.")])

    state_choices = [
            ('', ''), ('AL', 'Alabama'),('AK','Alaska'),
            ('AZ', 'Arizona'), ('AR', 'Arkansas'),
            ('CA', 'California')]

    event_location_state = SelectField('State',
            [validators.DataRequired()],
            choices=state_choices)

    event_location_zip = StringField('Zip',
            [validators.Length(min=5, max=5,
                message="Zip code must be 5 digits long")])

    # Generate a users list for invitees
    db = DB()
    db.connect()
    usersList = [(user.userName, user.firstName + " " + user.lastName)
            for user in db.getAllVerifiedUsers()]

    charitiesList = [(str(charity.charityID), charity.charityName)
            for charity in db.get_allCharities()]

    db.disconnect()

    event_invitees_list = MultiCheckboxField('Invitees',
            choices=usersList)

    event_charities_list = MultiCheckboxField('Charities',
            choices=charitiesList,
            option_widget = widgets.CheckboxInput())

    def __init__(self, *args, **kwargs):
        '''
        Initializer for event, no event is default.
        '''
        Form.__init__(self, *args, **kwargs)
        self.event = None

    def validate(self):
        '''
        Handles validating the event form data entered in.
        '''

        # Validate our form first
        rv = Form.validate(self)
        if not rv:
            return False

        # This is how you fetch the invitees & charities selection
        # Returns as a list

        # Perform some unique validations
        isValidated = True
        # Make sure there's at least one guest invited
        if len(self.event_invitees_list.data) == 0:
            flash('Please invite at least one guest')
            isValidated = False

        # Make sure there's at least one charity selected
        if len(self.event_charities_list.data) == 0:
            flash('Please select at least one charity')
            isValidated = False

        if not isValidated:
            return False

        db = DB()
        db.connect()
        # Make sure there's no event already in place
        # TODO: Add query check if there's another event

        # If there's no event in place, create a new event
        # TODO: Add a query to create a new event
        # new_event = <CREATE_QUERY>
        new_event = None

        # TODO: Create function to add the users/invitees as well

        db.disconnect()

        # Set the login form's user
        self.event = new_event
        return True

class LoginForm(Form):
    '''
    Login class for validating user accounts by
    username and password.
    '''
    username = StringField('Username', [validators.Length(min=2, max=25)])
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

        # Connect to DB
        db = DB()
        db.connect()

        # Fetch the user
        user = db.get_user(self.username.data)
        db.disconnect()

        # Validate the account's username-pw
        if user is None:
            # No user found
            self.username.errors.append('Invalid login!')
            return False

        if not user.verify_password(self.password.data):
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

    firstname = StringField('First Name', [
        validators.DataRequired(),
        validators.Length(min=2)
    ])
    lastname = StringField('Last Name')
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

    # TODO: Validation on phone? If entered, needs to be certain length
    phone = StringField('Phone Number', [validators.Length(max=10)])

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

        # TODO: Now, insert the new user onto the DB

        db = DB()
        db.connect()

        new_user = db.create_user(self.username.data, self.password.data,
                self.firstname.data, self.lastname.data, self.email.data,
                self.phone.data)

        db.disconnect()

        # Set the login form's user
        self.user = new_user
        return True

class EditAccountForm(Form):
    '''
    Edit account settings/details form class and validation
    '''

    firstname = StringField('First Name', [
        validators.DataRequired(),
        validators.Length(min=2)
    ])

    lastname = StringField('Last Name')

    # TODO: Validation on phone? If entered, needs to be certain length
    phone = StringField('Phone Number', [validators.Length(max=10)])

    old_password = PasswordField('Current Password')

    new_password = PasswordField('New Password',[
        validators.EqualTo('confirm', message='Passwords must match!')
    ])

    confirm = PasswordField('Repeat Password')

    def __init__(self, *args, **kwargs):
        '''
        Initializer for signup
        '''
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def populate_fields(self, user):
        '''
        Function populates the fields
        '''

        self.firstname.data = user.firstName
        self.lastname.data = user.lastName
        self.phone.data = user.phoneNumber


    def validate(self):
        '''
        Handles validating the changed account information
        '''

        # Validate our form first
        rv = Form.validate(self)
        if not rv:
            return False

        # Perform extra validation steps
        # Make sure old password is correct if
        # the form is updating the pw
        db = DB()
        db.connect()

        # TODO: Query to see if the email or username is already taken

        # TODO: Now, insert the new user onto the DB

        db = DB()
        db.connect()

        new_user = db.create_user(self.username.data, self.password.data,
                self.firstname.data, self.lastname.data, self.email.data,
                self.phone.data)

        db.disconnect()

        # Set the login form's user
        self.user = new_user
        return True

