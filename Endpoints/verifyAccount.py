from flask_restful import Resource, current_app
import jwt
from bson import ObjectId

class VerifyAccount(Resource):
    def get(self, verificationToken):
        try:
            payload = jwt.decode(verificationToken, current_app.config["SECRET_KEY_VERIFICATION"], algorithms=['HS256'])

            mongo = current_app.extensions['mongo']
            userId = ObjectId(payload['sub'])

            user_exists = mongo.db.users.find_one({"_id": userId})

            if not user_exists:
                return "User does not exist", 400

            result = mongo.db.users.update_one({"_id": userId}, {"$set": {"isVerified": True}})


            if result.modified_count > 0:
                return "User was successfully verified", 200
            else:
                return "User already verified", 400
            
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please request to reset your password one more time.', 400
        except jwt.InvalidTokenError:
            return 'Invalid token. Please request to reset your password one more time.', 400
