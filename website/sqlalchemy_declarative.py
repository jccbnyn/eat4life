import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	# Here we define columns for the table user
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	
# Create an engine that stores data in the local directory's 
# sqlalchemy_example.db file
engine = create_engine('sqlite:///user.db', echo=True)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

