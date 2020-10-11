from flask                   import jsonify, Blueprint
from flask_request_validator import GET, Param, validate_params

def create_event_endpoints(event_service, Session):
    #Blueprint 설정
    event_app = Blueprint('event_app', __name__, url_prefix='/api/events')
    
    @event_app.route('', methods = ['GET'])
    @validate_params(
        Param('is_deleted', GET, int, required = False),
        Param('limit',      GET, int, required = False, default = 30),
        Param('offset',     GET, int, required = False),
    )
    def select_event_list(*args):
        """ 상품 정보 전달 API
        여러 상품 정보가 필요한 페이지에서 쿼리 파라미터로 필터링에 사용될 값을 받아 필터링된 상품의 데이터들을 표출합니다.

        args:
            *args:
                is_deleted : 진행중인지 종료인지 여부
                limit : pagination 을 위한 파라미터
                offset : pagination 을 위한 파라미터

        returns :
            상품리스트

        Authors:
            권창식

        History:
            2020-10-10 (권창식): 초기 생성
        """
        session = Session()
        try:
            event_info = {
                'is_deleted' : args[0],
                'limit'      : args[1],
                'offset'     : args[2]
            }
            get_event_list = event_service.select_event_list(event_info, session)
            event_list     = [dict(event_list) for event_list in get_event_list]
            print(event_list)
            if not event_list:
                return jsonify({'message' : 'EMPTY_DATA'}), 400
            return jsonify({'data' : event_list}), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()
    
    return event_app