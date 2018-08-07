from flask_restplus import Namespace, Resource, fields
from app.blueprints.api.models import CharacterModel


ns = Namespace("characters", description="Characters related operations.")


character_api_model = ns.model(
    "Character",
    {
        "name_romaji": fields.String(required=True, description="The character's name in romaji"),
        "name_kanji": fields.String(required=True, description="The character's name in kanji"),
        "is_not_in_manga": fields.Boolean(required=True, description="True if the character did not appear in the original mange"),
    },
)


@ns.route("/")
class CharacterList(Resource):
    @ns.doc("get_character_list")
    @ns.marshal_list_with(character_api_model)
    def get(self):
        """Fetch all characters."""
        characters = CharacterModel.find_all()
        return characters


@ns.route("/<int:character_id>")
@ns.param("character_id", "The character's identifier")
class Character(Resource):
    @ns.doc("get_character", responses={404: "Character not found."})
    @ns.marshal_with(character_api_model)
    def get(self, character_id):
        """Fetch a character given its identifier."""
        character = CharacterModel.find_by_id(character_id)
        if character is None:
            ns.abort(404, message="Character not found.")
        else:
            return character, 200


@ns.route("/random")
class CharacterRandom(Resource):
    @ns.doc("get_character_random")
    @ns.marshal_with(character_api_model)
    def get(self):
        """Fetch a random character."""
        character = CharacterModel.random()
        return character, 200
