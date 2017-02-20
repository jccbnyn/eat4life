# Import the ORM objects from Model.py
from Model import User, Charity, CharityMember, CharityEvent, CharityEventInvitees, loadSession

# Import the database conn. obj. from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import datetime

class DB:
    """
    This class contains database functions such as create, read, update,
    delete a user, charity, charity event.
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


#----------------------------- User Functions ------------------------

    def get_user_by_id(self, user_id):
        """
        Get the user based on user ID.
        Function expects a int user_id to be passed in.
        """
        # Create a new session and query for a user
        session = loadSession()
        user = session.query(User).filter(User.userID == user_id).first()
        session.close()
        return user


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
        user = (session.query(User).filter(
            User.userName == passedInUserName).first())
        session.close()
        return user


    def get_allUsers(self):
        """
        Args:
                none
        Returns:
                All the users stored in the database.
        Raises:
                Exception if there are no users saved,
                i.e., zero users, in the db
        """
        # Create a new session
        session = loadSession()
        # Query for all users
        allUsers = session.query(User).all()
        # Check if query was successful
        if allUsers == None:
            session.close()
            raise Exception("Users not found.")
        else:
            session.close()
            return allUsers


    def create_user(self, new_userName, new_password, new_firstName,
            new_lastName, new_emailAddress, new_phoneNumber):
        """ Creates a user and saves it in the database.

        Args:
                new: _username, _password, _firstName,
                _lastName, _emailAddress, _phoneNum
        Returns:
                A new user with the specified args in the user table.
        Raises:
                Exception if the user info was not saved properly.
        """
        # Can't have empty username, password, firstname, email
        if str(new_userName) == '':
            raise Exception("User Can't have empty username")
        if str(new_password) == '':
            raise Exception("User Can't have empty password")
        if str(new_firstName) == '':
            raise Exception("User Can't have empty firstname")
        if str(new_emailAddress) == '':
            raise Exception("User Can't have empty emailaddress")

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
        # Commit/Save the record in the database
        session.commit()
        # Check if it's saved properly
        user = (session.query(User).filter(
            User.userName == new_userName).first())
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
        """ This function deletes an existing user
            in the database given a userName

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
        user = (session.query(User).filter(
            User.userName == passedInUserName).first())

        if user != None:
            session.rollback()
            session.close()
            raise Exception("userName "
                    + str(passedInUserName)
                    + " was not deleted. Rolling back")


    def verify_user_by_id(self, user_id):
        """
        Function activates the user account & sets the flag.
        """
        # Create a new session & query
        session = loadSession()
        user = session.query(User).filter(User.userID == user_id).first()

        # Check if user currently exists in db
        if user == None:
            session.close()
        else:
            # Update user to verified
            user.isEmailVerified = True
            user.emailVerifiedDate = datetime.datetime.now()
            session.commit()
            session.close()


    def update_user(self, passedInUserName, new_userName, new_firstName,
            new_lastName, new_email, new_phone):
        """ Updates an existing user in the database

        Args:
                passedInUserName - The user to update
                new_userName - The user's new username
                new_firstName - The user's new first name
                new_lastName - The user's new last name
                new_email - The user's new email address
                new_phone - The users' new phone number
        Returns:
                The user with the new information passed in
        Raises:
                Exception if the passedInUsername does not exist in the db.
        """
        # Can't have empty username, firstname, email
        if str(new_userName) == '':
            raise Exception("User Can't have empty username")
        if str(new_firstName) == '':
            raise Exception("User Can't have empty firstname")
        if str(new_email) == '':
            raise Exception("User Can't have empty email")

        # Create a new session & query
        session = loadSession()
        user = (session.query(User).filter(
            User.userName == passedInUserName).first())

        # Check if user currently exists in db
        if user == None:
            session.close()
            raise Exception("userName "
                    + str(passedInUserName)
                    + " does NOT exist. "
                    + "Can't update a non-existent user.")
        else:
            # Update user row with new values
            user.userName = str(new_userName)
            user.firstName = str(new_firstName)
            user.lastName = str(new_lastName)
            user.emailAddress = str(new_email)
            user.phoneNumber = str(new_phone)
            # Save the update
            session.commit()

        # Verify that the update was successful
        updated_user = session.query(User).filter(
                User.userName == new_userName).first()
        if updated_user == None:
            session.rollback()
            session.close()
            raise Exception("username " + str(new_userName) + " not found.")
        else:
            session.close()
            return updated_user


#---------------------- Charity Event Functions ------------------------

    def get_allCharityEvents(self):
        """
        Args:
                none
        Returns:
                All the charity events stored in the database.
        Raises:
                Exception if there are no charity events saved,
                i.e., zero events, in the db
        """
        # Create a new session
        session = loadSession()
        # Query for all 
        allEvents = session.query(CharityEvent).all()
        # Check if query was successful
        if allEvents == None:
            session.close()
            raise Exception("Charity Events not found.")
        else:
            session.close()
            return allEvents
    
    
    def get_charityEvent_by_id(self, passedInCharityEventId):
        """
        Args:
                passedInCharityEventId - The charity event's id
        Returns:
                The charity event object with given id
        Raises:
                Exception if no such charity event is found
        """
        # Create a new session and query for a charity event
        session = loadSession()
        charityEvent = session.query(CharityEvent).filter(CharityEvent.charityEventID == passedInCharityEventId).first()
        session.close()
        return charityEvent      
	
	
    def create_charityEvent(self, new_eventName, new_dateTime, new_loc_streetAddr,
            new_loc_city, new_loc_state, new_loc_zip, new_loc_country, charityId):
        """ Creates a charity event and saves it in the database.

        Args:
                The charity event's name; date time; location as in street address, city name, state, zip code, country; and the id of the charity this event is associated with.
        Returns:
                A new charity event with the specified args in the user table.
        Raises:
                Exception if the charity event info was not saved properly.
        """        
        # Can't have empty event name, dateTime, and location 
        if str(new_eventName) == '':
            raise Exception("Charity Event Can't have empty event name")
        if str(new_dateTime) == '':
            raise Exception("Charity Event Can't have empty dateTime")
        if str(new_loc_streetAddr) == '':
            raise Exception("Charity Event Can't have empty street address")
        if str(new_loc_city) == '':
	    raise Exception("Charity Event Can't have empty city name")
        if str(new_loc_state) == '':
	    raise Exception("Charity Event Can't have empty state name")
	if str(new_loc_zip) == '':
	    raise Exception("Charity Event Can't have empty zip code")
	if str(new_loc_country) == '':
            raise Exception("Charity Event Can't have empty country name")
        if(str(charityId) == ''):
            raise Exception("Charity Event Can't have an empty charity id")
            
        # Create a new session
        session = loadSession()
        # Create a new charity event
        new_charityEvent = CharityEvent(str(new_eventName),
                new_dateTime,
                str(new_loc_streetAddr),
                str(new_loc_city),
                str(new_loc_state),
                str(new_loc_zip),
                str(new_loc_country),
                charityId)
                
        # Add new charity event
        session.add(new_charityEvent)
        # Commit/Save the record in the database
        session.commit()
        # Check if it's saved properly
        charityEvent = (session.query(CharityEvent).filter(
            CharityEvent.charityEvent_name == new_eventName).first())
        if charityEvent != None:
            print '\nCreated charity event successfully\n'
            session.close()
            return charityEvent
        else:
            # Otherwise, charity event was not saved properly, rollback save
            print '\nDid not create charity event\n'
            session.rollback()
            session.close()
            raise Exception("Did not save correctly")	
	

    def delete_charityEvent(self, passedInCharityEventId):
        """ This function deletes an existing charity event
            in the database given a charity event id

        Args:
                The charity event id
        Returns:
                No object
        Raises:
                Exception if the passed-in charity event does not exist in the db
        """
        # Create a new session & query
        session = loadSession()
        charityEvent = session.query(CharityEvent).filter(CharityEvent.charityEventID == passedInCharityEventId)
        # Check if charity event currently exists in db
        if charityEvent.first() == None:
            # if not, raise an Exception and close the session
            session.close()
            raise Exception("charity event id " + str(passedInCharityEventId) + " NOT found")
        else:
            charityEvent.delete()
            session.commit()

        # Verify that the row has been deleted
        charityEvent = (session.query(CharityEvent).filter(
            CharityEvent.charityEventID == passedInCharityEventId).first())
        if charityEvent != None:
            session.rollback()
            session.close()
            raise Exception("Charity Event Id "
                    + str(passedICharityEventId)
                    + " was not deleted. Rolling back")	


    def update_charityEvent(self, passedInCharityEventId, update_eventName, update_dateTime,
            update_loc_streetAddr, update_loc_city, update_loc_state, update_loc_zip, update_loc_country):
        """ Updates an existing charity event in the database

        Args:
                passedInCharityEventId - The charity event to update
                update_eventName - The charity event's new name
                update_dateTime - The charity event's new date and time
                update_loc_streetAddr - The charity event's new street address
                update_loc_city - The charity event's new city name
                update_loc_state - The charity event's new state
                update_loc_zip - charity event's new zip code
                update_loc_country - charity event's new country
        Returns:
                The charity event with the new information passed in
        Raises:
                Exception if the passedInCharityEventId does not exist in the db.
        """
        # Can't have empty event name, dateTime, and location 
        if str(update_eventName) == '':
            raise Exception("Charity Event Can't have empty event name")
        if str(update_dateTime) == '':
            raise Exception("Charity Event Can't have empty dateTime")
        if str(update_loc_streetAddr) == '':
            raise Exception("Charity Event Can't have empty street address")
        if str(update_loc_city) == '':
            raise Exception("Charity Event Can't have empty city name")
        if str(update_loc_state) == '':
            raise Exception("Charity Event Can't have empty state name")
	if str(update_loc_zip) == '':
            raise Exception("Charity Event Can't have empty zip code")
	if str(update_loc_country) == '':
            raise Exception("Charity Event Can't have empty country name")	

        # Create a new session & query
        session = loadSession()
        charityEvent = (session.query(CharityEvent).filter(
            CharityEvent.charityEventID == passedInCharityEventId).first())
        # Check if charity event currently exists in db
        if charityEvent == None:
            session.close()
            raise Exception("Charity Event Id "
                    + str(passedInCharityEventId)
                    + " does NOT exist. "
                    + "Can't update a non-existent charity event.")
        else:
            # Update charity event row with new values
            charityEvent.charityEvent_name = str(update_eventName)
            charityEvent.charityEvent_datetime = update_dateTime
            charityEvent.charityEvent_loc_streetAddr = str(update_loc_streetAddr)
            charityEvent.charityEvent_loc_city = str(update_loc_city)
            charityEvent.charityEvent_loc_state = str(update_loc_state)
            charityEvent.charityEvent_loc_zipcode = str(update_loc_zip)
            charityEvent.charityEvent_loc_country = str(update_loc_country)            
            
            # Save the update
            session.commit()

        # Verify that the update was successful
        updated_charityEvent = session.query(CharityEvent).filter(
                CharityEvent.charityEvent_name == update_eventName).first()
        if updated_charityEvent == None:
            session.rollback()
            session.close()
            raise Exception("Charity Event name " + str(update_eventName) + " not found.")
        else:
            session.close()
            return updated_charityEvent
            
            
#----------------------------- Charity Functions ------------------------

    def get_allCharities(self):
        """
        Args:
                none
        Returns:
                All the charities stored in the database.
        Raises:
                Exception if there are no charities saved,
                i.e., zero charities, in the db
        """
        # Create a new session
        session = loadSession()
        # Query for all charities
        allCharities = session.query(Charity).all()
        # Check if query was successful
        if allCharities == None:
            session.close()
            raise Exception("Charities not found.")
        else:
            session.close()
            return allCharities


    def get_charity(self, passedInCharityName):
        """
        Args:
                passedCharityName - The charity's name
        Returns:
                The charity object with given charity name
        Raises:
                Exception if no such charity is found
        """
        # Create a new session and query for a charity
        session = loadSession()
        charity = (session.query(Charity).filter(
            Charity.charityName == passedInCharityName).first())
        session.close()
        return charity


    def get_charity_by_id(self, passedInCharityId):
        """
        Args:
                passedInCharityId - The charity's id
        Returns:
                The charity object with given id
        Raises:
                Exception if no such charity is found
        """
        # Create a new session and query for a charity
        session = loadSession()
        charity = session.query(Charity).filter(Charity.charityID == passedInCharityId).first()
        session.close()
        return charity     


    def create_charity(self, new_charityName, new_address, new_email, new_phone):
        """ Creates a charity and saves it in the database.

        Args:
                The charity's name, address, email, and phone number information as String
        Returns:
                A new charity with the specified args in the user table.
        Raises:
                Exception if the charity info was not saved properly.
        """
        # Can't have empty charity name, address, email, and phone 
        if str(new_charityName) == '':
            raise Exception("Charity Can't have empty charity name")
        if str(new_address) == '':
            raise Exception("Charity Can't have empty charity address")
        if str(new_email) == '':
            raise Exception("Charity Can't have empty email address")
        if str(new_phone) == '':
            raise Exception("Charity Can't have empty phone number")				

        # Create a new session
        session = loadSession()
        # Create a new charity event
        new_charity = Charity(str(new_charityName),
                str(new_address),
                str(new_email),
                str(new_phone))
        # Add new charity
        session.add(new_charity)
        # Commit/Save the record in the database
        session.commit()
        # Check if it's saved properly
        charity = (session.query(Charity).filter(
            Charity.charityName == new_charityName).first())
        if charity != None:
            print '\nCreated charity successfully\n'
            session.close()
            return charity
        else:
            # Otherwise, charity was not saved properly, rollback save
            print '\nDid not create charity\n'
            session.rollback()
            session.close()
            raise Exception("Did not save correctly")	
	

    def delete_charity(self, passedInCharityName):
        """ This function deletes an existing charity event
            in the database given a charity name

        Args:
                The charity name
        Returns:
                No object
        Raises:
                Exception if the passed-in charity name does not exist in the db
        """
        # Create a new session & query
        session = loadSession()
        charity = session.query(Charity).filter(Charity.charityName == passedInCharityName)
        # Check if charity currently exists in db
        if charity.first() == None:
            # if not, raise an Exception and close the session
            session.close()
            raise Exception("Charity name " + str(passedInCharityName) + " NOT found")
        else:
            charity.delete()
            session.commit()

        # Verify that the row has been deleted
        charity = (session.query(Charity).filter(
            Charity.charityName == passedInCharityName).first())
        if charity != None:
            session.rollback()
            session.close()
            raise Exception("Charity name "
                    + str(passedInCharityName)
                    + " was not deleted. Rolling back")
 
 
    def update_charity(self, passedInCharityId, update_charityName, update_address, update_email, update_phone):
        """ Updates an existing charity in the database

        Args:
                passedInCharityId - The charity to update
                update_charityName - The charity's new name
                update_address - The charity's new address
                update_email- The charity's new email address
                update_phone - The charity's new phone number
        Returns:
                The charity with the new information passed in
        Raises:
                Exception if the passedInCharityId does not exist in the db.
        """
        # Can't have empty charity name, address, email, and phone 
        if str(update_charityName) == '':
            raise Exception("Charity Can't have empty charity name")
        if str(update_address) == '':
            raise Exception("Charity Can't have empty address")
        if str(update_email) == '':
            raise Exception("Charity Can't have empty email")
        if str(update_phone) == '':
            raise Exception("Charity Can't have empty phone number")

        # Create a new session & query
        session = loadSession()
        charity = (session.query(Charity).filter(
            Charity.charityID == passedInCharityId).first())
        # Check if charity currently exists in db
        if charity == None:
            session.close()
            raise Exception("Charity Id "
                    + str(passedInCharityId)
                    + " does NOT exist. "
                    + "Can't update a non-existent charity.")
        else:
            # Update charity row with new values
            charity.charityName = str(update_charityName)
            charity.charityAddress = str(update_address)
            charity.charityEmail = str(update_email)
            charity.charityPhone = str(update_phone)         
            
            # Save the update
            session.commit()

        # Verify that the update was successful
        updated_charity = session.query(Charity).filter(
                Charity.charityName == update_charityName).first()
        if updated_charity == None:
            session.rollback()
            session.close()
            raise Exception("Charity name " + str(update_charityName) + " not found.")
        else:
            session.close()
            return updated_charity
            
