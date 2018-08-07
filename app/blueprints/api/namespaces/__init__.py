"""Namespaces for the API.

A Flask-RESTPlus Namespace groups REST resources and links them to routes.
A RESTPlus Namespace is basically a Flask Blueprint for the API.

Several HTTP methods can be implemented for each route.
For a list of all HTTP methods supported by Flask-RESTPluss see:
https://flask-restplus.readthedocs.io/en/stable/_modules/flask/views.html?highlight=head

A resource is the EXTERNAL representation of an entity.
"""
from .characters import ns as characters
from .voice_actors import ns as voice_actors
from .fighting_styles import ns as fighting_styles
