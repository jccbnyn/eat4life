from website import site

# Setup key, externally visible, and debug mode
site.host = '0.0.0.0'
site.debug = True
site.secret_key = 'E474l1f3_@pW'

site.run()
