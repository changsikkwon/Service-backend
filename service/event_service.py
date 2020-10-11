class EventService:
    def __init__(self, event_dao):       
        self.event_dao = event_dao
    
    def select_event_list(self, event_info, session):
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
        event_list = self.event_dao.select_event_list(event_info, session)
        return event_list