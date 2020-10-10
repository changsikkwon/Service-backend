class EventDao:
    def select_event_list(self, is_deleted, session):
        """신규 order insert 로직
                    
        args:
            session : connection 형성된 session 객체
            user_id : 데코레이터 g객체 user_id
        
        return:
            유저가 주문한 모든 order_item
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """
        row = session.execute(
        """SELECT 
                id,
                banner_image
            FROM events
            WHERE e.is_deleted = :is_deleted
        """,{
            is_deleted : is_deleted   
        }).fetchall()
    
        return row