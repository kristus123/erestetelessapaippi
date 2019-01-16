from datetime import datetime
import requests
from flask import request, Blueprint	
from flask_restful import Api, Resource
from myapi.models import movies, User, rental_info
from flask_jwt_extended import jwt_required
from myapi.extensions import ma, db
from . import func

blueprint_api = Blueprint("movie_api", __name__)
movie_api = Api(blueprint_api)

class movieSchema(ma.ModelSchema):
	class meta:
		model = movies
		sqla_session = db.session

@movie_api.resource("/get_all_movies")
class get_all_movies(Resource):
	def get(self):
		x = movies.query.all()
		movieschema = movieSchema(many=True)
		return ({"info" :{"movies": movieschema.dump(x).data,
						"proof that i have columns in the db": str(x[0].title)}}, 201)

@movie_api.resource('/search_movies')
class search_movies(Resource):
	def post(self):
		send = {}
		c = request.get_json()
		title = c['title']
		x = func.search_movies(title)
		for title in x:
			available = None
			movie = movies.query.filter_by(title=title).first()
			if movie:
				available = True
				if movie.rental:
					available = False	
			send[str(title)] = available
		return send


@movie_api.resource("/add_movie")
class add_movie(Resource):
	def post(self):
		c = request.get_json()
		title = (str(c["title"])).replace(" ", "+")
		resp = func.get_movie_info(title)
		info = (resp.json())
		title = info["Title"]
		
		plot = info["Plot"]
		Genre = info["Genre"]


		try:
			check = movies.query.filter_by(title=title).first()
			if (check) == None:
				movie = movies(title=title, desc=plot, category=Genre)
				#put this in a celery task ? ask JEFF BOI
				db.session.add(movie)
				db.session.commit()
				return ({"movie added": title},201)
			else:
				return {"error": "movie already added",
						"title": check.title}
		except Exception as e:
			return {"error": str(e)}

@movie_api.resource("/rent_movie")
class rent_movie(Resource):
	def post(self):
		now = datetime.now()
		c = request.get_json()
		user_id = c['user_id']
		title   = c['title']
		date = c["rented_to_date"]
		rented_to_date = datetime.strptime(date, "%d.%m.%Y")
		
		movie   = db.session.query(movies).filter_by(title=title).first()
		bruker  = db.session.query(User).get(int(user_id))






		if movie == None:
			return {"error": "does the movie exist ?"}
		elif not movie.rental:
			info = rental_info(movie=movie, rented_by=int(bruker.id), rented_to_date=rented_to_date, rental_info=movie)
			db.session.add(info)
			try:
				db.session.commit()
			except Exception as e:
				db.session.rollback()
				return {"error": str(e)}

			return {"rented by user_id": str(user_id),
					"bruker": str(info.rented_by),
					"movie.rental": str(movie.rental),
					"rental_info": str(info.rental_info)}
		else:
			return {"movie already rented": "sorry"}





@movie_api.resource("/get_movie_info")
class get_movie_info(Resource):
	def get(self):
		movie = movies.query.filter_by('')
		return {"hihi": "hoho"}