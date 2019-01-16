from flask import Blueprint
from flask_restful import Api

from myapi.api.resources import UserResource, UserList
from myapi.api.resources.movie import blueprint_api

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')