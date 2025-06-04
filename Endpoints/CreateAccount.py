from flask import current_app
from flask_restful import Resource, request
import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, Regexp
import jwt, requests, datetime, os, json

def hash_password(password):
        #TODO: add some pepper 
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

def username_exists(username):
    mongo = current_app.extensions["mongo"]
    collection = mongo.db.users

    user = collection.find_one({"username": username})

    if user:
        return True
    return False

def email_exists(email):
    mongo = current_app.extensions["mongo"]
    collection = mongo.db.users

    user = collection.find_one({"email": email})

    if user:
        return True
    return False

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
         DataRequired(), 
         Length(min=4, max=25, message="Username must be between 4 and 25 characters"),
         Regexp(r'^[a-zA-Z0-9_]+$', message="Username must contain only letters, numbers, or underscores.")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[
         DataRequired(), 
         Length(min=5, max=25,  message="Password must be between 5 and 25 characters"),
    ])  

class CreateAccount(Resource):
    def post(self):
        #TODO: validate input 
        form = CreateAccountForm(formdata=request.form)
        if not form.validate():
            first_field_error = next(iter(form.errors.values()))[0]
            return first_field_error, 400
            
        if username_exists(form.username.data):
            return 'Username already exists', 400
        if email_exists(form.email.data):
            return 'Email already exists', 400
            
        #TODO: possible add email verification option

        # hash the password
        hashed = hash_password(form.password.data)

        mongo = current_app.extensions['mongo']

        try:
            newUser = mongo.db.users.insert_one({
                "username": form.username.data,
                "email": form.email.data,
                "password": hashed,
                "isVerified": False
            })
        except Exception as e:
            print(e)
            return "Error creating account. Try again later.", 500

        #calculates expiration through iat and exp fields
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expiration time
            'iat': datetime.datetime.utcnow(),  # Issued at time
            'sub': str(newUser.inserted_id)  # Subject of the token (user identification)
        }
        
        token = jwt.encode(payload, current_app.config["SECRET_KEY_VERIFICATION"], algorithm='HS256')
        
        #TODO: EMAIL SERVICE!? 
        response = requests.post(current_app.config["EMAIL_SERVICE_URL"] + "/api/sendEmail", json={
            "subject": "WTM: Verify your account",
            "html": "<html><h1>Welcome to What's the Move</h1><p> We are so glad you decided to join! Please verify your account <a href='http://whatsthemoveasu.com/verifyAccount/" + str(token) + "'>here</a></p></html>",
            "recipients": [form.email.data]
        })

        if response.status_code == 500:
            mongo.db.users.delete_one({"_id": newUser.inserted_id})
            return "Error sending verification email. Try again later.", 500
        
        return "Successfully sent email!", 200
    
