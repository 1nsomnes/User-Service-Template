import jwt
import datetime
from flask import current_app, request
from flask_restful import Resource
import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[
         DataRequired()
    ])  


def verifyPassword(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

class SignIn(Resource):
    def post(self):
        form = SignInForm(formdata=request.form)
        if not form.validate():
            first_field_error = next(iter(form.errors.values()))[0]
            return first_field_error, 400

        mongo = current_app.extensions['mongo']
        SECRET_KEY = current_app.config["SECRET_KEY_TOKENIZATION"]

        collection = mongo.db.users
        user = collection.find_one({"email": form.email.data})

        if user and verifyPassword(form.password.data, user["password"]):
            #check if verified
            if not user["isVerified"]:
                return "Account not verified.", 403

            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),  # Token expiration time
                'iat': datetime.datetime.utcnow(),  # Issued at time
                'sub': str(user['_id'])  # Subject of the token (user identification)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return {"authToken" : token}, 200
        else:
            return "Could not verify credentials", 404