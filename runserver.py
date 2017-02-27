from website import site

# Setup key, externally visible, and debug mode
# TODO: Set the site's secret key in the config file
site.secret_key = 'E474l1f3_@pW'
site.run(host='0.0.0.0', debug=True)
