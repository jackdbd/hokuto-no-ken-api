"""Instantiate a WSGI application.

Since this Flask application uses the app factory pattern, this python module
can be used to instantiate the Flask app. This is useful when starting the WSGI
application with Gunicorn.

Usage:
    gunicorn --bind 0.0.0.0:$PORT --access-logfile - "app.wsgi:application"

See Also:
    http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    https://stackoverflow.com/a/25319752/3036129
"""
from .app import create_app

application = create_app()
