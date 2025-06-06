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
the rest I will write later ig im tired

## Production
This template is mostly intended for building out web applications super quickly as such it is meant to be a development server, **not a production server**. While this can be the base of a production web server I recommend you take the following considerations into mind: 
- Change it to a production Flask server
- Verification, there are two sections (marked with TODOs) one that only allows verified accounts to login and one that creates a verification URL for people to authenticate. I highly recommend enabling these.
- Rate limiting, there is no rate limiting... Not really much else to say there
- Add some pepper to the hashes 
- CORS, I really did random stuff with this to make things work so definitely make sure that this is configured right for your use case 

These are just the things that I can think of off the top of my head, please take careful consideration before putting something into prod!! 

## Future Changes
I'll make changes as I need this service for my projects.

## Small History (mostly just for me)
This service was originally made for an application that I was developing with my friend [Ryan](https://github.com/rkimbers) called [What's the Move](https://github.com/whatsthemoveasu). It was a simple event board but we had built out several microservices including a user service. I found myself reusing it frequently so now I've decided to make it into a template that I as well as other people can use.  
