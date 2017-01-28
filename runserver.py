from website import site

# Setup key, externally visible, and debug mode
site.secret_key = 'dev_key'
site.host = '0.0.0.0'
site.debug = True

site.run()
