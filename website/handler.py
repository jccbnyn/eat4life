from website import site
from Model import User, Charity, CharityMember
from DBComm import DB

@site.route('/', methods=['GET'])
@site.route('/helloWorld', methods=['GET'])
def Index():
    myDBObject = DB()



    myDBObject.connect()
    print "I'm connected!"
    
    jenni_user = myDBObject.create_user("jenni2", "test", "jenni", "c", "jenni@gmail.com", "123456789")
    print jenni_user

    #print myDBObject.get_user("j")
    #print myDBObject.get_user("j3")  
    
    
    myDBObject.disconnect()
    print "I'm not connected!"
    
    #Hello, world test
    return "Hello, world! "

	
