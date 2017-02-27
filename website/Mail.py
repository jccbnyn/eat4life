# Import flask mail
from flask.ext.mail import Mail, Message

class MailManager():
    '''
    Mail manager class that handles all things Mail!
    '''

    def __init__(self, site):
        '''
        Defines a new mail manager for the web site
        '''
        site.config.update(
                DEBUG=True,
                MAIL_SERVER='smtp.gmail.com',
                MAIL_PORT=465,
                MAIL_USE_SSL=True,
                MAIL_USERNAME='luis111290@gmail.com',
                MAIL_PASSWORD='vgrpxciabbxzszsp')

        self.mail = Mail(site)

    def sendMail(self, email_address, title, body):
        '''
        Function handles sending an email to the provided
        email address with the title and body specified.
        '''
        # TODO: Should we return a bool for whether or not successfully sent?
        # TODO: Fix the sender, this should be passed in from a config file
        msg = Message(title,
                sender='luis111290@gmail.com',
                recipients=[email_address])
        msg.body = body
        self.mail.send(msg)

    def sendEventInviteesEmail(self, list_of_users, charity_event):
        '''
        Function shall handle sending an email invite to a charity event
        to the provided email addresses.
        '''
        # TODO: Fetch the event invite email template to use
        template = EventInviteEmailTemplate(list_of_users, charity_event)


class EventInviteEmailTemplate():
    '''
    The event invite email template helper class.
    This class handles generating the template to send out when
    an event's invite email is sent out.
    '''

    def __init__(self, list_of_users, charity_event):
        '''
        Set the template details
        '''
        self.list_of_users = list_of_users
        self.charity_event = charity_event


    def generateEmailBody():
        '''
        Function generates the email body template based on the
        event's details
        '''
        date = self.charity_event
        time = self.charity_event
        loc = (self.charityEvent_loc_streetAddr + ", "
                + self.charityEvent_loc_city + ", "
                + self.charityEvent_loc_state + ", "
                + self.charityEvent_loc_zipcode)


        body = """\
                <html>
                <head></head>
                <body>
                <p>You are invited to an event!
                <br>Date:{0}<br>
                <br>Time:{1}<br>
                <br>Location:{2}<br>
                Reply:
                <a href="http://www.python.org">ACCEPT</a>
                <a href="http://www.python.org">DECLINE</a>
                </p>
              </body>
            </html>
            """ % (date, time, loc)

