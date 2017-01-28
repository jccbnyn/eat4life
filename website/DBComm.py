# Import the ORM objects from Model.py
from Model import User, Charity, CharityMember, loadSession

# Import the database conn. obj. from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class DB:
	"""
	This class contains database functions such as create, read, update, 
	and delete a user.
	
	"""
	
	
	def __init__(self):
		self.database = None
	
	def connect(self, host = 'localhost'):
		"""
		Args:
			
		Returns:
			No object
		Raises:
			Exception if can't connect to the database
		"""
		try:
			if host == 'localhost':
				engine = create_engine('sqlite:///model.db', echo=False)
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
	
		
	def get_user(self, passedInUserName):
		"""
		Args:
			passedInUserName - The user's user name
		Returns:
			The user object with given username
		Raises:
			Exception if no such user is found
		"""
		
		# Create a new session and query for a user
		session = loadSession()
		user = session.query(User).filter(User.userName == passedInUserName).first()
		print "User found! " + str(user)
		
		# if there's no such user
		if user == None:
			session.close()
			raise Exception("userName " + passedInUserName + " not found/no such user")
		
		return user	
		
		
	def create_user(self, new_userName, new_password, new_firstName, 
		new_lastName, new_emailAddress, new_phoneNumber):
		"""Creates a user and saves it in the database.
		
		Args:
			new: _username, _password, _firstName, _lastName, _emailAddress, _phoneNum
		Returns:
			A new user with the specified args in the user table.
		Raises:
			Exception if the user info was not saved properly.
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
			# Otherwise, user was not saved properly, rollback save
			print '\nDid not create user\n'
			session.rollback()
			session.close()
			
			raise Exception("Did not save correctly")
	
	
	def delete_user(self, passedInUserName):
		"""This function deletes an existing user in the database given a userName
			
		Args:
			The user's userName
		Returns:
			No object
		Raises:
			Exception if the passed-in username does not exist in the db
		"""
		
		# Create a new session & query
		session = loadSession()
		user = session.query(User).filter(User.userName == passedInUserName)
		
		# Check if user currently exists in db
		if user.first() == None:
			# if not, raise an Exception and close the session
			session.close()
			raise Exception("userName " + str(passedInUserName) + " NOT found")
		else:
			user.delete()
			session.commit()
			
		# Verify that the row has been deleted
		user = session.query(User).filter(User.userName == passedInUserName).first()
		if user != None:
			session.rollback()
			session.close()
			raise Exception("userName " + str(passedInUserName) + " was not deleted. Rolling back")
		
		
		
		
	# read user
	# update user
	# delete user
