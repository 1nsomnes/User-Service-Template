from flask import Flask, jsonify, current_app
from flask_restful import Resource, Api, reqparse
import os
from flask_cors import CORS
from flask_pymongo import PyMongo
from Endpoints.signIn import SignIn
from dotenv import load_dotenv

from Endpoints.CreateAccount import CreateAccount
from Endpoints.verifyAccount import VerifyAccount
from Endpoints.secureEndpoint import SecureEndpoint

load_dotenv()

# Configuration
SECRET_KEY_SESSION = os.environ.get('SECRET_KEY_SESSION')
SECRET_KEY_VERIFICATION = os.environ.get('SECRET_KEY_VERIFICATION')

# Initialize Flask App
app = Flask(__name__)

# Retrieve MongoDB credentials from environment variables
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'root')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'example')
MONGO_DBNAME = "userDatabase"
MONGO_HOST = "localhost:27017"

mongo_uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DBNAME}?authSource=admin"

app.config["MONGO_URI"] = mongo_uri
app.config['WTF_CSRF_ENABLED'] = False

app.config["SECRET_KEY_SESSION"] = SECRET_KEY_SESSION
app.config["SECRET_KEY_VERIFICATION"] = SECRET_KEY_VERIFICATION

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

api = Api(app, prefix="/api")
CORS(app)

mongo = PyMongo(app)
app.extensions['mongo'] = mongo

# Resource Routing
api.add_resource(CreateAccount, '/createAccount')
api.add_resource(SignIn, '/signIn')
api.add_resource(VerifyAccount, '/verifyAccount/<string:verificationToken>')
api.add_resource(SecureEndpoint, '/secureEndpoint')

if __name__ == '__main__':
    # 0.0.0.0 allows users on the local network to access the API
    app.run(host= '0.0.0.0', port=5001)
