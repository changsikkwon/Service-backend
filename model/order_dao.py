class OrderDao:
    def insert_orders(self, order_info, user_id, session):
        """신규 order insert 로직
                    
        args:
            session    : connection 형성된 session 객체
            user_id    : 데코레이터 g객체 user_id
            order_info : order, order_item 정보
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """
        session.execute(
        """INSERT INTO orders (
                user_id,
                total_shipping_fee,
                total_discount,
                total_payment,
                shipping_memo,
                orderer_name,
                orderer_phone,
                orderer_email,
                receiver_name,
                receiver_phone,
                receiver_address,
                payment_date,
                created_at,
                is_deleted
             )
            VALUES(
                :user_id,
                :total_shipping_fee,
                :total_discount,
                :total_payment,
                :shipping_memo,
                :orderer_name,
                :orderer_phone,
                :orderer_email,
                :receiver_name,
                :receiver_phone,
                :receiver_address,
                now(),
                now(),
                0
        )"""
        ,{
        'user_id'             : user_id['user_id'],
        'shipping_address_id' : order_info['shipping_address_id'],
        'total_shipping_fee'  : order_info['total_shipping_fee'],
        'total_discount'      : order_info['total_discount'],
        'total_payment'       : order_info['total_payment'],
        'shipping_memo'       : order_info['shipping_memo'],
        'orderer_name'        : order_info['orderer_name'],
        'orderer_phone'       : order_info['orderer_phone'],
        'orderer_email'       : order_info['orderer_email'],
        'receiver_name'       : order_info['receiver_name'],
        'receiver_phone'      : order_info['receiver_phone'],
        'receiver_address'    : order_info['receiver_address'],
        }).lastrowid
        
        session.execute(
        """INSERT INTO order_item_info (
                order_detail_id,
                order_id,
                order_status_id,
                product_id,
                price,
                option_color,
                option_size,
                option_additional_price,
                units,
                discount_price,
                start_date,
                end_date,
                is_deleted
             )
            VALUES(
                (select concat(curdate()+0, LPAD(last_insert_id(),5,'0'))),
                (last_insert_id()),
                1,
                :product_id,
                :price,
                :option_color,
                :option_size,
                :option_additional_price,
                :units,
                :discount_price,
                now(),
                "9999-12-31 23:59:59",
                0
        )"""
        ,{
        'product_id'              : order_info['product_id'],
        'price'                   : order_info['price'],
        'option_color'            : order_info['option_color'],
        'option_size'             : order_info['option_size'],
        'option_additional_price' : order_info['option_additional_price'],
        'units'                   : order_info['units'],
        'discount_price'          : order_info['discount_price'],
        })
    
    def select_order_item(self, user_id, session):
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
                p_info.name,
                p_info.main_img,
                o.total_payment,
                o.user_id,
                o.created_at,
                o_item.id,
                o_item.option_size,
                o_item.option_color,
                o_item.units,
                o_item.price,
                o_item.order_detail_id,
                o_item.order_status_id,
                s_info.korean_name
            FROM order_item_info AS o_item
            INNER JOIN orders AS o ON o_item.order_id = o.id
            INNER JOIN products AS p ON o_item.product_id = p.id
            INNER JOIN product_info AS p_info ON p.id = p_info.product_id
            INNER JOIN sellers AS s ON p_info.seller_id = s.id
            INNER JOIN seller_info AS s_info ON s.id = s_info.seller_id
            WHERE o.user_id = :user_id
            AND o_item.is_deleted = 0
        """,{
            'user_id'  : user_id['user_id']
        }).fetchall()
    
        return row
    
    def end_record(self, order_detail_id, now, session):
        """order_item 선분 종료 로직
                    
        args:
            session         : connection 형성된 session 객체
            user_id         : 데코레이터 g객체 user_id
            order_detail_id : 선분종료 할 order_detail_id
            
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """
        session.execute(
        """ UPDATE order_item_info
            SET end_date = :now,
                is_deleted = 1
            WHERE order_detail_id = :order_detail_id
            AND is_deleted = 0
        """
        ,{
            'order_detail_id' : order_detail_id['order_detail_id'],
            'now'             : now
        })
    
    def insert_cancel_reason(self, cancel_reason, now, session):
        """order_item cancel 로직
                    
        args:
            session       : connection 형성된 session 객체
            now           : 현재시각
            cancel_reason : 취소하려는 order_item의 order_detail_id
            
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """
        session.execute(
         """INSERT INTO order_item_info (
                order_detail_id,
                order_id,
                order_status_id,
                product_id,
                price,
                option_color,
                option_size,
                option_additional_price,
                units,
                discount_price,
                start_date,
                end_date,
                cancel_reason_id
            )
            SELECT
                order_detail_id,
                order_id,
                6,
                product_id,
                price,
                option_color,
                option_size,
                option_additional_price,
                units,
                discount_price,
                :now,
                '9999-12-31 23:59:59',
                1
            FROM order_item_info
            WHERE is_deleted = 1
            AND order_detail_id = :order_detail_id
        """
        ,{
            'order_detail_id'  : cancel_reason['order_detail_id'],
            'now'              : now
        })
        
    def insert_refund_reason(self, refund_reason, now, session):
        """order_item refund 로직
                    
        args:
            session       : connection 형성된 session 객체
            now           : 현재시각
            refund_reason : 환불하려는 order_item의 order_detail_id, refund_reason_id
            
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """
        session.execute(
         """INSERT INTO order_item_info (
                order_detail_id,
                order_id,
                order_status_id,
                product_id,
                price,
                option_color,
                option_size,
                option_additional_price,
                units,
                discount_price,
                start_date,
                end_date,
                refund_reason_id
            )
            SELECT
                order_detail_id,
                order_id,
                7,
                product_id,
                price,
                option_color,
                option_size,
                option_additional_price,
                units,
                discount_price,
                :now,
                '9999-12-31 23:59:59',
                :refund_reason_id
            FROM order_item_info
            WHERE is_deleted = 1
            AND order_detail_id = :order_detail_id
        """
        ,{
            'refund_reason_id' : refund_reason['refund_reason_id'],
            'order_detail_id'  : refund_reason['order_detail_id'],
            'now'              : now
        })
        
    def insert_refund_cancel(self, refund_cancel, now, session):
        """order_item refund_cancel 로직
                    
        args:
            session       : connection 형성된 session 객체
            now           : 현재시각
            refund_cancel : 환불취소하려는 order_item의 order_detail_id
            
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-05 (권창식) : 초기 생성
        """
        session.execute(
         """INSERT INTO order_item_info (
                order_detail_id,
                order_id,
                order_status_id,
                product_id,
                price,
                option_color,
                option_size,
                option_additional_price,
                units,
                discount_price,
                start_date,
                end_date,
                refund_reason_id
            )
            SELECT
                order_detail_id,
                order_id,
                3,
                product_id,
                price,
                option_color,
                option_size,
                option_additional_price,
                units,
                discount_price,
                :now,
                '9999-12-31 23:59:59',
                Null
            FROM order_item_info
            WHERE is_deleted = 1
            AND order_detail_id = :order_detail_id
        """
        ,{
            'order_detail_id'  : refund_cancel['order_detail_id'],
            'now'              : now
        })