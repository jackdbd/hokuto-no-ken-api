from flask_restplus import Namespace, Resource, fields
from ..models.fighting_style import FightingStyleModel


ns = Namespace("fighting_styles", description="Fighting styles related operations.")


character_in_fighting_style = ns.model(
    "Character who uses this fighting style",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "name_romaji": fields.String(required=False),
        "name_kanji": fields.String(required=False),
        "url": fields.String(required=False),
    },
)


fighting_style_api_model = ns.model(
    "Fighting Style",
    {
        "id": fields.String(required=True, description="The fighting style's id"),
        "name": fields.String(required=True, description="The fighting style"),
        "url": fields.String(
            required=False, description="URL to the fighting style's wiki"
        ),
        "characters": fields.List(fields.Nested(character_in_fighting_style)),
    },
)


@ns.route("/")
class FightingStyleList(Resource):
    @ns.doc("get_fighting_style_list")
    @ns.marshal_list_with(fighting_style_api_model)
    def get(self):
        """Fetch all fighting styles."""
        fighting_styles = FightingStyleModel.find_all()
        return fighting_styles


@ns.route("/<string:fighting_style_id>")
@ns.param("fighting_style_id", "The fighting style's identifier")
class FightingStyle(Resource):
    @ns.doc("get_fighting_style", responses={404: "Fighting style not found."})
    @ns.marshal_with(fighting_style_api_model)
    def get(self, fighting_style_id):
        """Fetch a fighting style given its identifier."""
        fighting_style = FightingStyleModel.find_by_id(fighting_style_id)
        if fighting_style is None:
            ns.abort(404, message="Fighting style not found.")
        else:
            return fighting_style, 200


@ns.route("/random")
class FightingStyleRandom(Resource):
    @ns.doc("get_fighting_style_random")
    @ns.marshal_with(fighting_style_api_model)
    def get(self):
        """Fetch a random fighting style."""
        fighting_style = FightingStyleModel.random()
        return fighting_style, 200
