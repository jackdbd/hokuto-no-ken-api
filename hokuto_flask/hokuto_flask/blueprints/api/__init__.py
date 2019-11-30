from flask import Blueprint
from flask_restplus import Api
from .namespaces import characters, voice_actors, fighting_styles


api_blueprint = Blueprint(name="api", import_name=__name__, url_prefix="/api/v1")


api = Api(
    api_blueprint,
    version="1.0.0",
    title="API",
    description="Hokuto no Ken API. Powered by Flask-RESTPlus.",
)

# Remove the default namespace (not sure if this is the right way to do it).
api.namespaces.pop()

api.add_namespace(ns=characters, path="/characters")
api.add_namespace(ns=voice_actors, path="/voice_actors")
api.add_namespace(ns=fighting_styles, path="/fighting_styles")
