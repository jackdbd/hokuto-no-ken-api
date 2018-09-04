from flask_restplus import Namespace, Resource, fields
from ..models import CategoryModel


ns = Namespace("categories", description="Categories related operations.")

character_in_category = ns.model(
    "Character who belongs to this category",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "name_romaji": fields.String(required=False),
        "name_kanji": fields.String(required=False),
        "url": fields.String(required=False),
    },
)

category_api_model = ns.model(
    "Category",
    {
        "id": fields.String(required=True, description="The category's id"),
        "name": fields.String(required=True, description="The category's name"),
        "url": fields.String(required=False, description="URL to the category's wiki"),
        "characters": fields.List(fields.Nested(character_in_category)),
    },
)


@ns.route("/")
class CategoryList(Resource):
    @ns.doc("get_category_list")
    @ns.marshal_list_with(category_api_model)
    def get(self):
        """Fetch all categories."""
        categories = CategoryModel.find_all()
        return categories


@ns.route("/<string:category_id>")
@ns.param("category_id", "The category's identifier")
class Category(Resource):
    @ns.doc("get_category", responses={404: "Category not found."})
    @ns.marshal_with(category_api_model)
    def get(self, category_id):
        """Fetch a category given its identifier."""
        category = CategoryModel.find_by_id(category_id)
        if category is None:
            ns.abort(404, message="Category not found.")
        else:
            return category, 200


@ns.route("/random")
class CategoryRandom(Resource):
    @ns.doc("get_category_random")
    @ns.marshal_with(category_api_model)
    def get(self):
        """Fetch a random category."""
        category = CategoryModel.random()
        return category, 200
