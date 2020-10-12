import datetime

class OrderService:
    def __init__(self, order_dao):       
        self.order_dao = order_dao
    
    def insert_orders(self, order_info, user_id, session):
        """ order 등록 로직
   
        args:
            session    : connection 형성된 session 객체
            user_id    : 데코레이터 g객체 user_id
            order_info : order, order_item 정보
        
        returns:
            order insert 성공여부
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-04 (권창식) : 초기 생성
        """   
        new_order = self.order_dao.insert_orders(order_info, user_id, session)
        return new_order
    
    def select_order_item(self, user_id, session):
        """ order select 로직
                       
        args:
            session : connection 형성된 session 객체
            user_id : 데코레이터 g객체 user_id
        
        returns:
            유저의 모든 구매 상품
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-04 (권창식) : 초기 생성
        """   
        order_item_info = self.order_dao.select_order_item(user_id, session)
        return order_item_info
    
    def insert_cancel_reason(self, cancel_info, user_id, session):
        """ order_item 취소 로직
                       
        args:
            session     : connection 형성된 session 객체
            user_id     : 데코레이터 g객체 user_id
            cancel_info : 취소하려는 상품 주문 상세번호
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """ 
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.order_dao.end_record(cancel_info, now, session)
        check_order_item = self.order_dao.check_order_item(cancel_info, user_id, session)
        if not check_order_item:      
            self.order_dao.insert_cancel_reason(cancel_info, now, session)
    
    def insert_refund_reason(self, refund_info, user_id, session):
        """ order_item 환불 로직
                       
        args:
            session     : connection 형성된 session 객체
            user_id     : 데코레이터 g객체 user_id
            refund_info : 환불하려는 상품 주문 상세번호
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """ 
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.order_dao.end_record(refund_info, now, session)
        check_order_item = self.order_dao.check_order_item(refund_info, user_id, session)
        if not check_order_item:
            self.order_dao.insert_refund_reason(refund_info, now, session)
        
    def insert_refund_cancel(self, refund_cancel, user_id, session):
        """ order_item 환불취소 로직
                       
        args:
            session     : connection 형성된 session 객체
            user_id     : 데코레이터 g객체 user_id
            refund_info : 환불취소하려는 상품 주문 상세번호
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """ 
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.order_dao.end_record(refund_cancel, now, session)
        check_order_item = self.order_dao.check_order_item(refund_cancel, user_id, session)
        if check_order_item:
            self.order_dao.insert_refund_cancel(refund_cancel, now, session)