from flask import Blueprint
from flask_restplus import Api
from app.blueprints.api.namespaces import characters, voice_actors


blueprint = Blueprint(name="api", import_name=__name__, url_prefix="/api/v1")


api = Api(
    blueprint,
    version="1.0.0",
    title="API",
    description="Hokuto no Ken API. Powered by Flask-RESTPlus."
)

# Remove the default namespace (not sure if this is the right way to do it).
api.namespaces.pop()

api.add_namespace(ns=characters, path="/characters")
api.add_namespace(ns=voice_actors, path="/voice_actors")

# How to export as Postman collection? It says it needs an application context.
# api.as_postman()
