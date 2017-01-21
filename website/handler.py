from website import site
from Model import User, Charity, CharityMember

@site.route('/', methods=['GET'])
@site.route('/helloWorld', methods=['GET'])
def Index():
    #Hello, world test
    return "Hello, world!"
