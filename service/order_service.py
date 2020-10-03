class OrderService:
    def __init__(self, order_dao):       
        self.order_dao = order_dao
    
    def insert_orders(self, order_info, user_id, session):        
        new_order = self.order_dao.insert_orders(order_info, user_id, session)
        return new_order
    
    def select_order_item(self, user_id, session):
        order_item_info = self.order_dao.select_order_item(user_id, session)
        return order_item_info
    
    def update_cancel_reason(self, cancel_info, user_id, session):
        cancel_reason_info = self.order_dao.update_cancel_reason(cancel_info, user_id, session)
        return cancel_reason_info
    
    def update_refund_reason(self, refund_info, user_id, session):
        refund_reason_info = self.order_dao.update_refund_reason(refund_info, user_id, session)
        return refund_reason_info