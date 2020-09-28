class OrderDao:
    def insert_orders(order_info, session):
        """order, order_item insert 로직
                
        args :
            order_info : order 정보
        
        returns :
            마지막 insert row id
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-26 (권창식) : 초기 생성
        """
                
        row = session.execute(
        """INSERT INTO orders (
                user_id,
                shipping_address_id,
                total_shipping_fee,
                total_discount,
                total_payment,
                shipping_memo,
                orderer_name,
                orderer_phone,
                orderer_email,
                payment_date,
                created_at,
                is_deleted
             )
            VALUES(
                :user_id,
                :shipping_address_id,
                :total_shipping_fee,
                :total_discount,
                :total_payment,
                :shipping_memo,
                :orderer_name,
                :orderer_phone,
                :orderer_email,
                payment_date,
                now(),
                0
        )"""
        ,({
        'user_id'                 : order_info['user_id'],
        'shipping_address_id'     : order_info['shipping_address_id'],
        'total_shipping_fee'      : order_info['total_shipping_fee'],
        'total_discount'          : order_info['total_discount'],
        'total_payment'           : order_info['total_payment'],
        'shipping_memo'           : order_info['shipping_memo'],
        'orderer_name'            : order_info['orderer_name'],
        'orderer_phone'           : order_info['orderer_phone'],
        'orderer_email'           : order_info['orderer_email'],
        })).lastrowid
    
        return row
    
    def insert_order_item_info(order_item_info, session):
        """order, order_item insert 로직
                
        args :
            order_item_info : order_item 정보
        
        returns :
            마지막 insert row id
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-26 (권창식) : 초기 생성
        """
                
        row = session.execute(
        """INSERT INTO order_item_info (
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
                :order_id,
                1,
                :product_id,
                :price,
                :option_color,
                :option_size,
                :option_additional_price,
                :units,
                :discount_price,
                now(),
                9999-12-31 23:59:59,
                0
        )"""
        ,({
        'order_id'                : order_item_info['order_id'],
        'product_id'              : order_item_info['product_id'],
        'price'                   : order_item_info['price'],
        'option_color'            : order_item_info['option_color'],
        'option_size'             : order_item_info['option_size'],
        'option_additional_price' : order_item_info['option_additional_price'],
        'units'                   : order_item_info['units'],
        'discount_price'          : order_item_info['discount_price'],
        })).lastrowid
    
        return row

    def get_order_item(order_item_info_id, session):
        """구글유저 브랜디 회원가입 로직
                
        args :
            info_user : 구글에서 받아온 유저정보
        
        returns :
            회원가입 성공시 None
            실패시 에러발생
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
        row = session.execute((
        """SELECT 
                p_info.name,
                p_info.main_img,
                o.total_payment,
                o_item.option_size,
                o_item.option_color,
                o_item.units,
                o_item.price,
                s_info.korean_name
            FROM order_item_info AS o_item
            INNER JOIN orders AS o ON o_item.order_id = o.id
            INNER JOIN products AS p ON o_item.product_id = p.id
            INNER JOIN product_info AS p_info ON p.id = p_info.product_id
            INNER JOIN sellers AS s ON p_info.seller_id = s.id
            INNER JOIN seller_info AS s_info ON s.id = s_info.seller_id
            WHERE o_item.id = :order_item_info_id
        """), {'order_item_info_id' : order_item_info_id}).fetchall()
        
        return row