from flask                   import jsonify, Blueprint
from flask import json
from requests.sessions import extract_cookies_to_jar
from flask_request_validator import GET, Param, validate_params

def create_event_endpoints(event_service, Session):
    #Blueprint 설정
    event_app = Blueprint('event_app', __name__, url_prefix='/api/events')
    
    @event_app.route('', methods = ['GET'])
    @validate_params(
        Param('is_displayed', GET, int, required = False),
        Param('limit',        GET, int, required = False, default = 30),
        Param('offset',       GET, int, required = False),
    )
    def select_event_list(*args):
        """ event_list select endpoint 로직

        args:
            *args:
                limit  : pagination 을 위한 파라미터
                offset : pagination 을 위한 파라미터

        returns :
            event_list return

        Authors:
            권창식

        History:
            2020-10-10 (권창식): 초기 생성
        """
        session = Session()
        try:
            event_info = {
                'is_displayed' : args[0],
                'limit'        : args[1],
                'offset'       : args[2]
            }
            
            get_event_list = event_service.select_event_list(event_info, session)
            event_list     = [dict(event_list) for event_list in get_event_list]
            
            if not event_list:
                return jsonify({'message' : 'EMPTY_DATA'}), 400
            return jsonify({'data' : event_list}), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()
            
    @event_app.route('/detail', methods = ['GET'])
    @validate_params(
        Param('id', GET, int, required = False)
    )             
    def select_event_detail(*args):
        """ 상품 정보 전달 API
        여러 상품 정보가 필요한 페이지에서 쿼리 파라미터로 필터링에 사용될 값을 받아 필터링된 상품의 데이터들을 표출합니다.

        args:
            *args:
                id : event_id

        returns :
            event에 해당하는 정보 return

        Authors:
            권창식

        History:
            2020-10-10 (권창식): 초기 생성
        """
        session = Session()
        try:
            event_info = {'id' : args[0]}
            
            get_event_detail, get_event_button  = event_service.select_event_detail(event_info, session)
            
            if not get_event_detail:
                return jsonify({'message' : 'EMPTY_DATA'}), 400
            if not get_event_button:
                return jsonify({'message' : 'EMPTY_DATA'}), 400
            
            return jsonify({"event_detail" : get_event_detail,
                            "event_button" : get_event_button}), 200
     
        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()       
            
            
    @event_app.route('/products', methods = ['GET'])
    @validate_params(
        Param('id',        GET, int, required = True),
        Param('button_id', GET, int, required = True),
        Param('limit',     GET, int, required = False, default = 30),
        Param('offset',    GET, int, required = False),
    )             
    def select_event_products(*args):
        """ 상품 정보 전달 API
        여러 상품 정보가 필요한 페이지에서 쿼리 파라미터로 필터링에 사용될 값을 받아 필터링된 상품의 데이터들을 표출합니다.

        args:
            *args:
                id        : event_id 정보
                button_id : button_id 정보
                limit     : pagination 을 위한 파라미터
                offset    : pagination 을 위한 파라미터

        returns :
            event_products return

        Authors:
            권창식

        History:
            2020-10-10 (권창식): 초기 생성
        """
        session = Session()
        try:
            event_info = {
                'id'        : args[0],
                'button_id' : args[1],
                'limit'     : args[2],
                'offset'    : args[3]                
            }
            
            get_event_products = event_service.select_event_products(event_info, session)
            if not get_event_products:
                return jsonify({'message' : 'EMPTY_DATA'}), 400
            return jsonify({"event_product" : get_event_products}), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()                      
    
    return event_app