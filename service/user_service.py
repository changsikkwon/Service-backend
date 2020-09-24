import jwt

from config    import SECRET_KEY, ALGORITHM

class UserService:
    def __init__(self, user_dao):       
        self.user_dao = user_dao
    
    def get_or_create_google_user(self, user_info, session):
        user = self.user_dao.check_google_user(user_info, session)
        
        if not user:
            user = self.user_dao.insert_google_user(user_info, session)
            return user
        
        return dict(user)
    
    def generate_access_token(self, login_id):
        access_token = jwt.encode({'login_id' : login_id}, SECRET_KEY, ALGORITHM).decode('utf-8')
        return access_token