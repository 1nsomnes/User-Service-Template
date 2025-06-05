from flask_restful import Resource, current_app
import jwt
from bson import ObjectId
import datetime
from utils.requireSession import requireSession

class SecureEndpoint(Resource):
    method_decorators = [requireSession]

    def get(self, user_id):
        print(user_id) 
        return "Success", 400
