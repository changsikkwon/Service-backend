class OrderDao:
    def insert_orders(self, order_info, user_id, session):
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
        ,({
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
        })).lastrowid
        
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
                (select concat(curdate()+0, LPAD(last_insert_id(),4,'0'))),
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
        ,({
        'product_id'              : order_info['product_id'],
        'price'                   : order_info['price'],
        'option_color'            : order_info['option_color'],
        'option_size'             : order_info['option_size'],
        'option_additional_price' : order_info['option_additional_price'],
        'units'                   : order_info['units'],
        'discount_price'          : order_info['discount_price'],
        }))
    
    def select_order_item(self, order_id, user_id, session):
        row = session.execute((
        """SELECT 
                p_info.name,
                p_info.main_img,
                o.total_payment,
                o.user_id,
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
            WHERE o.user_id = :user_id
            AND o.id = :order_id
        """),{
            'user_id'  : user_id['user_id'],
            'order_id' : order_id['order_id']        
        }).fetchall()
        
        print(row)
        
        return row