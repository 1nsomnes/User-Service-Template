# User Service Template
A user service template that creates an authorization API in Flask and uses MongoDB. 
- Stores user data in MongoDB (yes I hashed the passwords and [added a lil salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) could use [some pepper though](https://en.wikipedia.org/wiki/Pepper_(cryptography))) 
- Creates session tokens using bcrypt
- Has decorators for protected endpoints

## How do I use it? 

Get the Mongo service up by running,
```
docker compose up
```
I would recommend creating a virtual python environment and then download the required libraries using the following command,
```
pip install -r requirements.txt
```
Finally, you should be able to run the service using,
```
python user_service.py
```

## How it works 

There are four end points listed below with example CURLs 
### Create Account
Link: _/api/createAccount_

Allows you to create account, requires a password, username, and email as a form.

```bash
curl localhost:5001/api/createAccount -X Post \
  -H "application/x-www-form-urlencoded" \
  -d "username=my_user&email=user@test.com&password=Password1"
```

### Sign In
Link: _/api/signIn_

Allows you to sign in and returns you a session which will expire in 30 days (this is easy to change via code)

```bash
curl localhost:5001/api/signIn -X Post \
  -H "application/x-www-form-urlencoded" \
  -d "username=my_user&password=Password1"
```

### Verify Account
Link: _/api/verifyAccount/<token>_

If you are using the verification capabilities use this endpoint to change a user from unverified to verified. 

```bash
curl localhost:5001/api/verifyAccount/sampleToken
```

### Secure Endpoint 
Link: _/api/secureEndpoint_

Use this to make sure that given a specific session you are able to access the a end point that is session protected 

```bash
curl localhost:5001/api/secureEndpoint \
  -H "Authorization: Bearer SessionToken" 
```

## Creating new endpoints 
If you want to extend this program, it is as simple as writing a new endpoint and adding it as a service like I've done for the last four endpoints.

```python
api.add_resource(CreateAccount, '/createAccount')
api.add_resource(SignIn, '/signIn')
api.add_resource(VerifyAccount, '/verifyAccount/<string:verificationToken>')
api.add_resource(SecureEndpoint, '/secureEndpoint')
```

To create an end point and a session protected endpoint please see the code below,
```python
from utils.requireSession import requireSession

class SecureEndpoint(Resource):
    method_decorators = [requireSession]

    def get(self, user_id):
        print(user_id) 
        return "Success", 400
```

As you can see, you can add method decorators to make it a session protected end point and the code for an endpoint in general is simple. Refer to the previous code snippert to see how you can add it to the service and you should be all set! 

## Production
This template is mostly intended for building out web applications super quickly as such it is meant to be a development server, **not a production server**. While this can be the base of a production web server I recommend you take the following considerations into mind: 
- Change it to a production Flask server
- Verification, there are two sections (marked with TODOs) one that only allows verified accounts to login and one that creates a verification URL for people to authenticate. I highly recommend enabling these.
- Rate limiting, there is no rate limiting... Not really much else to say there
- Add some pepper to the hashes 
- CORS, I really did random stuff with this to make things work so definitely make sure that this is configured right for your use case
- The databse is exposed on your local port (27017), remove the line in the compose doing this and wrap this as its own Docker service. 

These are just the things that I can think of off the top of my head, please take careful consideration before putting something into prod!! 

## Future Changes
I'll make changes as I need this service for my projects.

## Small History (mostly just for me)
This service was originally made for an application that I was developing with my friend [Ryan](https://github.com/rkimbers) called [What's the Move](https://github.com/whatsthemoveasu). It was a simple event board but we had built out several microservices including a user service. I found myself reusing it frequently so now I've decided to make it into a template that I as well as other people can use.  
