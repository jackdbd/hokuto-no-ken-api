from flask_restplus import Namespace, Resource, fields
from ..models import CharacterModel


ns = Namespace("characters", description="Characters related operations.")

voice_actor_in_character = ns.model(
    "Voice actor who dubbed this character",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "url": fields.String(required=False),
    },
)

fighting_style_in_character = ns.model(
    "Fighting style used by this character",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "url": fields.String(required=False),
    },
)

category_in_character = ns.model(
    "Category on Hokuto Renkitōza where this character can be found",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "url": fields.String(required=False),
    },
)

family_member_in_character = ns.model(
    "Family member of this character",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "name_romaji": fields.String(required=False),
        "name_kanji": fields.String(required=False),
        "url": fields.String(required=False),
    },
)


character_api_model = ns.model(
    "Character",
    {
        "id": fields.String(required=True, description="The character's id"),
        "name": fields.String(required=True, description="The character's name"),
        "name_romaji": fields.String(
            required=False, description="The character's name (in romaji)"
        ),
        "name_kanji": fields.String(
            required=False, description="The character's name (in kanji)"
        ),
        "avatar": fields.String(
            required=False, description="The character's avatar on Hokuto Renkitōza"
        ),
        "url": fields.String(
            required=False, description="The character's wiki URL on Hokuto Renkitōza"
        ),
        "first_appearance_anime": fields.Integer(
            required=False,
            description="The first anime episode where the character appears",
        ),
        "first_appearance_manga": fields.Integer(
            required=False,
            description="The first manga chapter where the character appears",
        ),
        "voice_actors": fields.List(fields.Nested(voice_actor_in_character)),
        "fighting_styles": fields.List(fields.Nested(fighting_style_in_character)),
        "categories": fields.List(fields.Nested(category_in_character)),
        "right_relatives": fields.List(fields.Nested(family_member_in_character)),
        "left_relatives": fields.List(fields.Nested(family_member_in_character)),
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


@ns.route("/<string:character_id>")
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
