from flask          import request, Blueprint, jsonify, g

from util           import login_required

def create_order_endpoints(user_service, Session):
    # Blueprint 설정
    order_app = Blueprint('order_app', __name__, url_prefix='/api/order')
    
    @order_app.route("/", methods = ['POST'], endpoint = 'insert_order')
    @login_required
    def insert_order():
        """ 구글로그인 로직
        구글유저 정보 요청 후 DB데이터 확인 후 토큰발행
        
        args :
            session : connection 형성된 session 객체
        
        returns :
            user access_token
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
        session = Session()
        try:
            order_info     = request.json
            user_id        = g.user_id
            print(user_id)
            new_order_info = user_service.insert_order(order_info, user_id, session)
            
            return jsonify({'message' : new_order_info}), 200
            
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
        finally:
            session.close()
            
    @order_app.route("/item", methods = ['POST'], endpoint = 'insert_order_item_info')
    def insert_order_item_info():
        """ 구글로그인 로직
        구글유저 정보 요청 후 DB데이터 확인 후 토큰발행
        
        args :
            session : connection 형성된 session 객체
        
        returns :
            user access_token
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
        session = Session()
        try:
            order_item_info     = request.json
            new_order_itme_info = user_service.insert_order(order_item_info)
            
            return jsonify({'message' : new_order_itme_info}), 200
            
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
        finally:
            session.close()
    
    return order_app