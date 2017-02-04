from sqlalchemy import Column, Integer, String, Float, DateTime, \
        Boolean, create_engine, ForeignKey
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
        return '<User(%d, %s, %s, %s)>' % (self.userID, self.userName, self.firstName, self.lastName)

    def validate_password(self, password):
        """ Checks that an unhashed password matches one that has previously been hashed
        """
        return bcrypt.checkpw(password, self.password)

    def check_password(self, password):
        '''
        Function checks the password of the User vs. passed in pw
        '''
        return (self.password == password)


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
        return '<Charity(%d, %s)>' % (self.charityID, self.charityName)


class CharityMember(Base):
    __tablename__ = 'charity_member'
    # Here we define columns for the "charity_member" table
    charityMemberID = Column(Integer, primary_key=True, nullable=False)
    charityMember_userID = Column(Integer, ForeignKey("user.userID"))
    charityMember_charityID = Column(Integer, ForeignKey("charity.charityID"))

    # variable names
    charityMember_User = relationship(
            "User", foreign_keys=[charityMember_userID])
    charityMember_Charity = relationship(
            "Charity", foreign_keys=[charityMember_charityID])

    def __init__(self, charityMember_userID, charityMember_charityID):
        self.charityMember_userID = charityMember_userID
        self.charityMember_charityID = charityMember_charityID

    def __repr__(self):
        return '<CharityMember(%d, %s, %s)>' % (self.charityMemberID,
        self.charityMember_userID, self.charityMember_charityID)


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def loadSession():
    return Session()
