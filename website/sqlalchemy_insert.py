import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import User, Base

engine = create_engine('sqlite:///user.db', echo=True)
# Bind the engine to the metadata of the Base class so that the 
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

# Create a session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert User(s) in the user table
new_user = User(name='new user')
session.add(new_user)
new_user = User(name='jenn')
session.add(new_user)

# Commit the record in the database
session.commit()

