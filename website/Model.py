from sqlalchemy import Column, Integer, String, Float, DateTime, \
        Boolean, create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ForeignKeyConstraint
import bcrypt

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


class Charity(Base):
    __tablename__ = 'charity'
    # Here we define columns for the "charity" table
    charityID = Column(Integer, primary_key=True, nullable=False)
    charityName = Column(String(length=30), nullable=False)
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
	charityEvent_datetime = Column(DateTime, default=func.now())
	charityEvent_loc_streetAddr = Column(String(length=30))
	charityEvent_loc_city = Column(String(length=30))
	charityEvent_loc_state = Column(String(length=2))
	charityEvent_loc_zipcode = Column(String(length=5))
	charityEvent_loc_country = Column(String(length=30))
	charityEvent_charityID = Column(Integer, ForeignKey("charity.charityID"))
	
	# foreign key
	charityEvent_Charity = relationship("Charity", foreign_keys=[charityEvent_charityID])
	
	def __init__(self, charityEvent_name, charityEvent_datetime, charityEvent_loc_streetAddr, 
	charityEvent_loc_city, charityEvent_loc_state, charityEvent_loc_zipcode, charityEvent_loc_country):
		self.charityEvent_name = charityEvent_name
		self.charityEvent_datetime = charityEvent_datetime
		self.charityEvent_loc_streetAddr = charityEvent_loc_streetAddr
		self.charityEvent_loc_city = charityEvent_loc_city
		self.charityEvent_loc_state = charityEvent_loc_state
		self.charityEvent_loc_zipcode = charityEvent_loc_zipcode
		self.charityEvent_loc_country = charityEvent_loc_country
		
	def __repr__(self):
		return ('<CharityEvent(%s, %s, %s)>' % (self.charitEvent_name, 
		self.charityEvent_datetime, self.charityEvent_loc_streetAddr))


class CharityEventAttendees(Base):
	__tablename__ = 'charity_event_attendees'
	charityEventAttendeesID = Column(Integer, primary_key=True, nullable=False)
	charityEventAttendees_isHost = Column(Boolean, unique=False, default=False)
	charityEventAttendees_charityEventID = Column(Integer, ForeignKey("charity_event.charityEventID"))
	charityEventAttendees_userID = Column(Integer, ForeignKey("user.userID"))
	
	# foreign keys
	charityEventAttendees_User = relationship("User", foreign_keys=[charityEventAttendees_userID])
	charityEventAttendees_CharityEvent = relationship("CharityEvent", foreign_keys=[charityEventAttendees_charityEventID])
	
	def __init__(self, charityEventAttendees_isHost, charityEventAttendees_charityEventID, charityEventAttendees_userID):
		self.charityEventAttendees_isHost = charityEventAttendees_isHost
		self.charityEventAttendees_charityEventID = charityEventAttendees_charityEventID
		self.charityEventAttendees_userID = charityEventAttendees_userID
		
	def __repr__(self):
		return ('<CharityEventAttendees(%s, %d %d)>' % (self.charityEventAttendees_isHost, 
		charityEventAttendees_charityEventID, charityEventAttendees_userID))
	

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def loadSession():
    return Session()
