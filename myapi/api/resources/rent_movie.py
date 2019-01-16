from flask_restful import Resource, Api
from flask import Blueprint


rent = Blueprint("rent_api", __name__)
r = Api(rent)


@r.resource("/rent_movie")
class rent_movie(Resource):
	def get(self):
		available = True
		return {"available": available}
	def post(self):
		return {"hei": "der"}