class EventService:
    def __init__(self, event_dao):       
        self.event_dao = event_dao
    
    def select_event_list(self, event_info, session):
        """ event_list select 로직
    
        args:
            session    : connection 형성된 session 객체
            event_info : limit, offset 정보
        returns:
            event_info의 조건에 해당하는 이벤트 return
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-12 (권창식) : 초기 생성
        """   
        event_list = self.event_dao.select_event_list(event_info, session)
        return event_list
    
    def select_event_detail(self, event_info, session):
        """ event_detail select 로직
           
        args:
            session    : connection 형성된 session 객체
            event_info : event_id, limit, offset 정보
        returns:
            event_info의 조건에 해당하는 이미지, 버튼, 유투브 정보 return
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-12 (권창식) : 초기 생성
        """     
        event_detail_lists = self.event_dao.select_event_detail(event_info, session)
        event_buttons = self.event_dao.check_buttons(event_info, session)     
        return [dict(event_detail_list) for event_detail_list in event_detail_lists], [dict(event_button) for event_button in event_buttons]
    
    def select_event_products(self, event_info, session):
        """ event_prdoucts select 로직
           
        args:
            session    : connection 형성된 session 객체
            event_info : event_id, button_id, limit, offset 정보
        returns:
            event_info의 조건에 해당하는 상품들 return
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-12 (권창식) : 초기 생성
        """   
        if not event_info['button_id']:
            event_info['button_id'] = 0
        event_products = self.event_dao.select_event_products(event_info, session)      
        return [dict(event_product) for event_product in event_products]