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


    def get_user_by_id(self, user_id):
        """
        Get the user based on user ID
        """
        # TODO: Add doc string
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
        user = session.query(User).filter(User.userName == passedInUserName).first()
        session.close()
        return user


    def get_allUsers(self):
        """
        Args:
                none
        Returns:
                All the users stored in the database.
        Raises:
                Exception if there are no users saved, i.e., zero users, in the db
        """
        print "all the users below"
        # Create a new session
        session = loadSession()
        # Query for all users
        allUsers = session.query(User).all()
        # Check if query was successful
        if allUsers == None:
            session.close()
            raise Exception("Users not found.")
        else:
            print "\nAll the users: \n" + str(allUsers)
            session.close()
            return allUsers


    def create_user(self, new_userName, new_password, new_firstName,
            new_lastName, new_emailAddress, new_phoneNumber):
        """ Creates a user and saves it in the database.

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
        """ This function deletes an existing user in the database given a userName

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
            raise Exception("Can't have empty username")
        if str(new_firstName) == '':
            raise Exception("Can't have empty firstname")
        if str(new_email) == '':
            raise Exception("Can't have empty email")

        # Create a new session & query
        session = loadSession()
        user = session.query(User).filter(User.userName == passedInUserName).first()

        # Check if user currently exists in db
        if user == None:
            session.close()
            raise Exception("userName " + str(passedInUserName) + " does NOT exist. Can't update a non-existent user.")
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
        updated_user = session.query(User).filter(User.userName == new_userName).first()
        if updated_user == None:
            session.rollback()
            session.close()
            raise Exception("username " + str(new_userName) + " not found.")
        else:
            session.close()
            return updated_user


