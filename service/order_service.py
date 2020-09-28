class OrderService:
    def __init__(self, order_dao):       
        self.order_dao = order_dao
    
    def insert_order(self, order_info, session):
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
        order = self.order_dao.insert_orders(order_info, session)
        return order
    
    def insert_order_item_info(self, order_item_info, session):
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
        order_item_info = self.order_dao.insert_order_item_info(order_item_info, session)
        return order_item_info
    
    def get_order_item(self, user_info, session):
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