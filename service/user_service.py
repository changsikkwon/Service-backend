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
        """access_token 발행 로직
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
        """신규 배송지 insert 로직
                        
        args :
            shipping_address_info : user의 배송지 정보
            session : connection 형성된 session 객체
            user_id : 데코레이터 g객체 user_id
        
        returns :
            신규 배송지 lastrowid
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
            2020-10-06 (권창식) : shipping_address count 로직 추가
        """
        count_shipping_address = self.user_dao.count_shipping_address(user_id, session)
        if count_shipping_address < 5:
            is_default = 0
            if count_shipping_address == 0:
                is_default = 1
            new_shipping_address_info = self.user_dao.insert_shipping_address(shipping_address_info, user_id, is_default, session)
            return new_shipping_address_info
    
    def select_shipping_address(self, user_id, session):
        """배송지 select 로직
                        
        args :
            session : connection 형성된 session 객체
            user_id : 데코레이터 g객체 user_id
        
        returns :
            해당 유저의 모든 배송지정보
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
        """
        shipping_address_info = self.user_dao.select_shipping_address(user_id, session)
        return shipping_address_info
    
    def update_shipping_address(self, shipping_address_info, user_id, session):
        """배송지 update 로직
                        
        args :
            shipping_address_info : user의 배송지 수정 정보
            session : connection 형성된 session 객체
            user_id : 데코레이터 g객체 user_id
        
        returns :
            update lastrowid
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
        """
        shipping_address_info = self.user_dao.update_shipping_address(shipping_address_info, user_id, session)
        return shipping_address_info
    
    def delete_shipping_address(self, user_id, delete_info, session):
        """배송지 update 로직
                        
        args :
            delete_info : 삭제하고자하는 배송지 
            session : connection 형성된 session 객체
            user_id : 데코레이터 g객체 user_id
        
        returns :
            배송지정보
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
        """
        shipping_address_info = self.user_dao.delete_shipping_address(user_id, delete_info, session)
        return shipping_address_info    