import jwt

from flask      import request, g, jsonify

from config     import SECRET_KEY, ALGORITHM
from functools  import wraps

def login_required(func):      
    @wraps(func)                   
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization') 
        if access_token is not None:  
            try:
                payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM) 
            except jwt.InvalidTokenError:
                 payload = None

            if payload is None:
                return jsonify({'message' : 'INVALID_TOKEN'}), 401

            user_id   = payload
            g.user_id = user_id
            
        else:
            return jsonify({'message' : 'INVALID_TOKEN'}), 401

        return func(*args, **kwargs)
    return decorated_function