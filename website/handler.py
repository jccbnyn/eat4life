from website import site

@site.route('/', methods=['GET'])
@site.route('/helloWorld', methods=['GET'])
def Index():
    #Hello, world test
    return "Hello, world!"
