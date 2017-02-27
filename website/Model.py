from sqlalchemy import Column, Integer, String, Float, DateTime, \
        Boolean, create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ForeignKeyConstraint
import bcrypt
import datetime

# Create an engine that stores data in the local directory
engine = create_engine('sqlite:///model.db', echo=True)
Base = declarative_base(engine)

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the "user" table
    userID = Column(Integer, primary_key=True, nullable=False)
    userName = Column(String(length=30), unique=True, nullable=False)
    password = Column(String(length=30), nullable=False)
    firstName = Column(String(length=30), nullable=False)
    lastName = Column(String(length=30))
    emailAddress = Column(String(length=30), nullable=False)
    phoneNumber = Column(String(length=20))
    isEmailVerified = Column(Boolean, nullable=False, default=False)
    emailVerifiedDate = Column(DateTime)

    def __init__(self, userName, password, firstName, lastName,
            emailAddress, phoneNumber):
        self.userName = userName
        # Hash a password for the first time, with a randomly-generated salt
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.firstName = firstName
        self.lastName = lastName
        self.emailAddress = emailAddress
        self.phoneNumber = phoneNumber

    def __repr__(self):
        """
        To String for printing user
        """
        return ('<User(%d, %s, %s, %s)>'
                % (self.userID, self.userName, self.firstName, self.lastName))

    def verify_password(self, password):
        """
        Checks that an unhashed password matches
        one that has previously been hashed
        """
        pwhash = bcrypt.hashpw(
                password.encode('utf-8'), self.password.encode('utf-8'))
        return self.password == pwhash

    def is_active(self):
        """
        True, as all users are active.
        """
        # TODO: We must handle the logic for whether or not the user is
        # currently active
        return True

    def get_id(self):
        """
        Returns the user's ID
        """
        return self.userID

    def is_authenticated(self):
        """
        Return True if the user is authenticated.
        """
        # TODO: We must add a user login table to handle user logins and save
        # to the DB whether or not the user has an authenticated session
        return True

    def is_anonymous(self):
        """
        Returns False (anonymous users aren't supported)
        """
        return False


class Charity(Base):
    __tablename__ = 'charity'
    # Here we define columns for the "charity" table
    charityID = Column(Integer, primary_key=True, nullable=False)
    charityName = Column(String(length=30), unique=True, nullable=False)
    charityAddress = Column(String(length=30))
    charityEmail = Column(String(length=20))
    charityPhone = Column(String(length=20))

    def __init__(self, charityName, charityAddress, charityEmail,
            charityPhone):

        self.charityName = charityName
        self.charityAddress = charityAddress
        self.charityEmail = charityEmail
        self.charityPhone = charityPhone

    def __repr__(self):
        """
        To String for printing charity
        """
        return '<Charity(%d, %s)>' % (self.charityID, self.charityName)


class CharityMember(Base):
    __tablename__ = 'charity_member'
    # Here we define columns for the "charity_member" table
    charityMemberID = Column(Integer, primary_key=True, nullable=False)
    charityMember_userID = Column(Integer, ForeignKey("user.userID"))
    charityMember_charityID = Column(Integer, ForeignKey("charity.charityID"))

    # foreign keys
    charityMember_User = relationship(
            "User", foreign_keys=[charityMember_userID])
    charityMember_Charity = relationship(
            "Charity", foreign_keys=[charityMember_charityID])

    def __init__(self, charityMember_userID, charityMember_charityID):
        self.charityMember_userID = charityMember_userID
        self.charityMember_charityID = charityMember_charityID

    def __repr__(self):
        """
        To String for printing user
        """
        return ('<CharityMember(%d, %s, %s)>'
                % (self.charityMemberID, self.charityMember_userID,
                    self.charityMember_charityID))


class CharityEvent(Base):
    __tablename__ = 'charity_event'
    # Columns for the "charity_event" table
    charityEventID = Column(Integer, primary_key=True, nullable=False)
    charityEvent_name = Column(String(length=30))
    charityEvent_datetime = Column(DateTime)
    charityEvent_loc_streetAddr = Column(String(length=30))
    charityEvent_loc_city = Column(String(length=30))
    charityEvent_loc_state = Column(String(length=2))
    charityEvent_loc_zipcode = Column(String(length=5))
    charityEvent_loc_country = Column(String(length=30))
    # parent id:
    charityEvent_charityId = Column(Integer, ForeignKey('charity.charityID'))

    def __init__(self, charityEvent_name, charityEvent_datetime,
            charityEvent_loc_streetAddr,
            charityEvent_loc_city, charityEvent_loc_state,
            charityEvent_loc_zipcode,
            charityEvent_loc_country, charityEvent_charityId):

            self.charityEvent_name = charityEvent_name
            self.charityEvent_datetime = charityEvent_datetime
            self.charityEvent_loc_streetAddr = charityEvent_loc_streetAddr
            self.charityEvent_loc_city = charityEvent_loc_city
            self.charityEvent_loc_state = charityEvent_loc_state
            self.charityEvent_loc_zipcode = charityEvent_loc_zipcode
            self.charityEvent_loc_country = charityEvent_loc_country
            self.charityEvent_charityId = charityEvent_charityId

    def __repr__(self):
            return ('<CharityEvent(%s, %s, %s, %d)>' % (self.charityEvent_name,
                self.charityEvent_datetime, self.charityEvent_loc_streetAddr,
                self.charityEvent_charityId))


class CharityEventInvitee(Base):
    __tablename__ = 'charity_event_invitee'
    # Columns for "charity_event_invitee" table
    charityEventInviteeID = Column(Integer, primary_key=True, nullable=False)
    charityEventID = Column(Integer, ForeignKey('charity_event.charityEventID'))
    userID = Column(Integer, ForeignKey('user.userID'))
    isHost = Column(Boolean, unique=False, default=False)
    isAttending = Column(Boolean, unique=False, default=False)

    def __init__(self, charityEventInvitee_charityEventID,
            charityEventInvitee_userID, charityEventInvitee_isHost,
            charityEventInvitee_isAttending):

            self.charityEventID = charityEventInvitee_charityEventID
            self.userID = charityEventInvitee_userID
            self.isHost = charityEventInvitee_isHost
            self.isAttending = charityEventInvitee_isAttending


    #~ def __init__(self):
        #~ self.charityEventInvitee_isAttending = False
        #~ self.charityEventInvitee_isHost = False

    def get_isAttending(self):
        return self.isAttending

    def get_isHost(self):
        return self.isHost

    def set_isAttending(self, value):
        self.isAttending = value

    def set_isHost(self, value):
        self.isHost = value

    def __repr__(self):
            return ('<CharityEventInvitee(%d, %d, %s, %s)>' %
                    (self.charityEventID, self.userID, self.isHost,
                        self.isAttending))


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def loadSession():
    return Session()
