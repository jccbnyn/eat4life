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
