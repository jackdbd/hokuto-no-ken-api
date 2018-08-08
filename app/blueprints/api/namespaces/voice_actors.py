from flask_restplus import Namespace, Resource, fields
from ..models import VoiceActorModel


ns = Namespace("voice_actors", description="Voice Actors related operations.")


voice_actor_api_model = ns.model(
    "Voice Actor",
    {
        "id": fields.Integer(required=True, description="The voice actor's id"),
        "name": fields.String(required=True, description="The voice actor's name"),
        "url": fields.String(
            required=False, description="URL to the voice actor's wiki"
        ),
    },
)


@ns.route("/")
class VoiceActorList(Resource):

    @ns.doc("get_voice_actor_list")
    @ns.marshal_list_with(voice_actor_api_model)
    def get(self):
        """Fetch all voice actors."""
        voice_actors = VoiceActorModel.find_all()
        return voice_actors


@ns.route("/<int:voice_actor_id>")
@ns.param("voice_actor_id", "The voice actor's identifier")
class VoiceActor(Resource):

    @ns.doc("get_voice_actor", responses={404: "Voice actor not found."})
    @ns.marshal_with(voice_actor_api_model)
    def get(self, voice_actor_id):
        """Fetch a voice actor given its identifier."""
        voice_actor = VoiceActorModel.find_by_id(voice_actor_id)
        if voice_actor is None:
            ns.abort(404, message="Voice actor not found.")
        else:
            return voice_actor, 200


@ns.route("/random")
class VoiceActorRandom(Resource):

    @ns.doc("get_voice_actor_random")
    @ns.marshal_with(voice_actor_api_model)
    def get(self):
        """Fetch a random voice actor."""
        voice_actor = VoiceActorModel.random()
        return voice_actor, 200
