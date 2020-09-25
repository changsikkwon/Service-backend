import jwt

from config    import SECRET_KEY, ALGORITHM

class UserService:
    def __init__(self, user_dao):       
        self.user_dao = user_dao
    
    def check_google_user(self, user_info, session):
        """
        구글유저 DB 존재유무 확인 로직
                
        args :
            info_user : 구글에서 받아온 유저정보
        
        returns :
            유저정보
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """

        user = self.user_dao.check_google_user(user_info, session)
        
        if not user:
            return None
        
        return user
    
    def google_sign_up_user(self, user_info, session):
        """
        구글 신규 유저 회원가입
                
        args :
            info_user : 구글에서 받아온 유저정보, Input Phone_number, login_id
        
        returns :
            유저정보
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-25 (권창식) : 초기 생성
        """
        
        new_user_id = self.user_dao.insert_google_user(user_info, session)
        return new_user_id
    
    def generate_access_token(self, email):
        """ 
        access_token 발행 로직
            email 확인 후 토큰발행        
                
        args :
            email : 구글유저 email
        
        returns :
            access_token
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
        
        access_token = jwt.encode({'email' : email}, SECRET_KEY, ALGORITHM).decode('utf-8')
        return access_token