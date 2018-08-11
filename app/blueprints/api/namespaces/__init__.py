"""Namespaces for the API.

A Flask-RESTPlus Namespace groups REST resources and links them to routes.
A RESTPlus Namespace is basically a Flask Blueprint for the API.

A resource is the EXTERNAL representation of an entity.

Several HTTP methods can be implemented for each route.

See Also
    List of all HTTP methods supported by Flask-RESTPlus:
    https://flask-restplus.readthedocs.io/en/stable/_modules/flask/views.html
"""
from .characters import ns as characters
from .voice_actors import ns as voice_actors
from .fighting_styles import ns as fighting_styles
