# Import the ORM objects from Model.py
from Model import User, Charity, CharityMember, loadSession

# Import the database conn. obj. from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class DB:
	def __init__(self):
		self.database = None
	
	def connect(self, host = 'localhost'):
		try:
			if host == 'localhost':
				engine = create_engine('sqlite:///model.db', echo=True)
				self.database = engine.connect()
			else:
				# TODO: fix this later
				engine = create_engine('sqlite:///' + str(host), 
					echo=True)
				self.database = engine.connect()	
		except:
			raise Exception("Can't connect to the database")
			
	def disconnect(self):
		if self.database != None:
			self.database.close()
			self.database = None
	
		
	def get_user(self, userId):
		"""
		Args:
			userId - The user's user id
		Returns:
			The user object with given userId
		Raises:
			Exception if no such user is found
		"""
		# Create a new session and query for a user
		session = loadSession()
		user = session.query(User).filter(User.userID == userId).first()
		print user
		
		# if there's no such user
		if user == None:
			session.close()
			raise Exception("userId not found/no such user")
		
		return user	
		
		
	def create_user(self, new_userName, new_password, new_firstName, 
		new_lastName, new_emailAddress, new_phoneNumber):
		"""
		Args:
		
		Returns:
			A new user with the specified args in the user table.
		Raises:
			
		"""
	
		# Can't have empty username, password, firstname, email
		if str(new_userName) == '':
			raise Exception("Can't have empty username")
		if str(new_password) == '':
			raise Exception("Can't have empty password")
		if str(new_firstName) == '':
			raise Exception("Can't have empty firstname")
		if str(new_emailAddress) == '':
			raise Exception("Can't have empty emailaddress")	
		
		# Create a new session
		session = loadSession()
		
		# Create a new user
		new_user = User(str(new_userName), 
			str(new_password), 
			str(new_firstName), 
			str(new_lastName),
			str(new_emailAddress),
			str(new_phoneNumber))
			
		# Add new user
		session.add(new_user)
		# Commit the record in the database
		session.commit()
			
		# Check if it's saved properly	
		user = session.query(User).filter(User.userName == new_userName).first()
			
		if user != None:
			print '\nCreated user successfully\n'
			session.close()
			return user
		else:
			# Otherwise, user was not saved properly. Rollback save
			print '\nDid not create user\n'
			session.rollback()
			session.close()
			
			raise Exception("Did not save correctly")
		
		
