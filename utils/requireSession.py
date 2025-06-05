
from functools import wraps
from flask import request, abort, current_app
import jwt
from bson import ObjectId

def requireSession(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            abort(401, "Missing or malformed token header")

        token = auth.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY_SESSION"], algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            abort(401, "Session expired")

        except jwt.InvalidTokenError:
            abort(401, "Invalid session")

        user_id = payload.get("sub")
        if user_id is None:
            abort(401, "Token missing subject")

        # Inject user_id into the kwargs for the wrapped method
        kwargs["user_id"] = user_id
        return fn(*args, **kwargs)

    return wrapper
