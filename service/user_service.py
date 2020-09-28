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
        new_user_info = self.user_dao.insert_google_user(user_info, session)
        return new_user_info
    
    def generate_access_token(self, user_info):
        """ 
        access_token 발행 로직
            user_info 확인 후 토큰발행        
                
        args :
            user_info : 구글유저 user_info
        
        returns :
            access_token
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
        access_token = jwt.encode({'user_id' : user_info}, SECRET_KEY, ALGORITHM).decode('utf-8')
        return access_token
    
    def insert_shipping_address(self, shipping_address_info, user_id, session):
        new_shipping_address_info = self.user_dao.insert_shipping_address(shipping_address_info, user_id, session)
        if not new_shipping_address_info:
            return "FULL_SHIPPING_ADDRESS"
        return new_shipping_address_info
    
    def select_shipping_address(self, user_id, session):
        shipping_address_info = self.user_dao.select_shipping_address(user_id, session)
        return shipping_address_info
    
    def update_shipping_address(self, shipping_address_info, user_id, session):
        new_shipping_address_info = self.user_dao.update_shipping_address(shipping_address_info, user_id, session)
        return new_shipping_address_info
    
    def delete_shipping_address(self, user_id, delete_info, session):
        new_shipping_address_info = self.user_dao.delete_shipping_address(user_id, delete_info, session)
        return new_shipping_address_info    