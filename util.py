import jwt

from flask      import request, Response, g

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
                return Response(status = 401)  

            login_id   = payload['login_id']  
            g.login_id = login_id
            
        else:
            return Response(status = 401)  

        return f(*args, **kwargs)
    return decorated_function