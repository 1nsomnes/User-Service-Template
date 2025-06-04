from flask_restful import Resource, current_app
import jwt
from bson import ObjectId
import datetime

class isValidToken(Resource):
    def get(self, verificationToken):
        try:
            payload = jwt.decode(verificationToken, current_app.config["SECRET_KEY_SESSION"], algorithms=['HS256'])

            if payload['exp'] < datetime.datetime.utcnow().timestamp():
                print("token expired")
                return False, 403

            mongo = current_app.extensions['mongo']
            if not mongo.db.users.find_one({"_id": ObjectId(payload['sub'])}):
                return False, 200
            
            return True, 200
        except Exception as e:
            print(e)
            return False, 403

