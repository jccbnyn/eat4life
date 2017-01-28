import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import User, Base

engine = create_engine('sqlite:///user.db', echo=True)

# Create a session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create objects
for user in session.query(User).order_by(User.id):
	print user.id, user.name
	 
	 
for user in session.query(User).filter(User.name == 'jenn'):
	print user.id, user.name
