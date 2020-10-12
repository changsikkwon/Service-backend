class EventDao:
    def select_event_list(self, event_info, session):
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
                type_id,
                banner_image
            FROM events
            WHERE is_deleted = :is_deleted
            AND is_displayed = 1
            ORDER BY created_at DESC
            LIMIT :limit
            OFFSET :offset
        """,{
            'is_deleted' : event_info['is_deleted'],
            'limit'      : event_info['limit'],
            'offset'     : event_info['offset']
        }).fetchall()
        return row
    
    def select_event_youtube_button_detail(self, event_info, session):
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
                e_bt.button_name,
                e_bt.display_order,
                e_pd.button_id,
                e.simple_description,
                e.detail_description,
                e.video_url
            FROM events AS e
            LEFT JOIN event_button AS e_bt ON e.id = e_bt.event_id
            INNER JOIN event_product_mappings AS e_pd ON e.id = e_pd.event_id
            WHERE e.is_deleted = 0
            AND e.id = :id
        """,{
            'id' : event_info['id']
        }).fetchall()
         
        return row
    
    def select_event_products(self, event_info, session):
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
                e_pd.button_id,
                p_info.name,
                p_info.main_img AS image,
                p_info.price,
                s_info.korean_name AS seller_name
            FROM events AS e
            LEFT JOIN event_button AS e_bt ON e.id = e_bt.event_id
            INNER JOIN event_product_mappings AS e_pd ON e.id = e_pd.event_id
            INNER JOIN products AS p ON e_pd.product_id = p.id
            INNER JOIN product_info AS p_info ON p.id = p_info.product_id
            INNER JOIN sellers AS s ON p_info.seller_id = s.id
            INNER JOIN seller_info AS s_info ON s.id = s_info.seller_id
            WHERE e.is_deleted = 0
            AND e.id = :id
        """,{
            'id' : event_info['id']
        }).fetchall()
        
        return row