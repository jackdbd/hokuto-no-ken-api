"""Instantiate a WSGI application.

This Python module can be used to instantiate the Flask application.

Instantiating a Flask application this way is known as **App factory pattern**.

Since a Flask app is a WSGI application, the application instance can be passed
to a WSGI HTTP server such as Gunicorn (e.g. in a Procfile or in Dockerfile), or
it can be specified as the main entry point for AWS API Gateway (e.g. when
deploying the app with Zappa. See zappa_settings.json).

See Also:
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    https://stackoverflow.com/a/25319752/3036129
    https://github.com/Miserlou/Zappa#running-the-initial-setup--settings
"""
from hokuto_flask.app import create_app

application = create_app()
