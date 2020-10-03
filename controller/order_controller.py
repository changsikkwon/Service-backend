import simplejson

from flask          import request, Blueprint, jsonify, g

from util           import login_required

def create_order_endpoints(order_service, Session):
    # Blueprint 설정
    order_app = Blueprint('order_app', __name__, url_prefix='/api/order')
    
    @order_app.route("", methods = ['POST'], endpoint = 'insert_order')
    @login_required
    def insert_orders():
        session = Session()
        try:
            order_info     = request.json
            user_id        = g.user_id
            order_service.insert_orders(order_info, user_id, session)
            
            session.commit()
            return jsonify({'message' : 'SUCCESS'}), 200
        
        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400
            
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
        finally:
            session.close()
            
    @order_app.route("/item", methods = ['GET'], endpoint = 'select_order_item_info')
    @login_required
    def select_order_item_info():
        session = Session()
        try:
            user_id             = g.user_id
            get_order_item_info = order_service.select_order_item(user_id, session)
            order_item_info     = [dict(order_item_info) for order_item_info in get_order_item_info]
            
            return jsonify({'data' : order_item_info}), 200
            
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
        finally:
            session.close()
            
    @order_app.route("/cancel", methods = ['PUT'], endpoint = 'update_cancel_reason')
    @login_required
    def update_cancel_reason():
        session = Session()
        try:
            cancel_info          = request.json
            user_id              = g.user_id
            order_service.update_cancel_reason(cancel_info, user_id, session)
  
            return jsonify({'message' : 'SUCCESS'}), 200
        
        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400    
            
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
        finally:
            session.close()
            
    @order_app.route("/refund", methods = ['PUT'], endpoint = 'update_refund_reason')
    @login_required
    def update_refund_reason():
        session = Session()
        try:
            refund_info          = request.json
            user_id              = g.user_id
            order_service.update_refund_reason(refund_info, user_id, session)
  
            return jsonify({'message' : 'SUCCESS'}), 200
        
        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400    
            
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
        finally:
            session.close()

    return order_app