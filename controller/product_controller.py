from flask import jsonify, Blueprint
from flask_request_validator import (
    GET,
    PATH,
    Param,
    JSON,
    Enum,
    validate_params
)

def create_product_endpoints(product_service, Session):

    product_app = Blueprint('product_app', __name__, url_prefix='/api/products')

    @product_app.route('/category', methods = ['GET'])
    def product_category():
        """ 카테고리 정보 전달 API

        상위 카테고리에 따른 하위 카테고리 리스트를 전달합니다.

        returns :
            200: 카테고리 리스트
            500:

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-25 (고지원): 한 번의 쿼리로 3개의 카테고리 데이터를 전달하도록 수정
        """
        try:
            session = Session()
            category = product_service.get_menu(session)

            # 각 카테고리를 저장하기 위한 리스트
            second_category = []
            first_category = []
            main_category = []

            for i in category:
                if (i.m_id, i.main_category_name) not in main_category:
                    # 메인 카테고리 리스트
                    main_category.append((i.m_id, i.main_category_name))
                if (i.f_id, i.first_category_name, i.main_category_id) not in first_category:
                    # 첫 번째 데이터 리스트
                    first_category.append((i.f_id, i.first_category_name, i.main_category_id))
                # 세 번째 카테고리 리스트
                second_category.append((i.s_id, i.second_category_name, i.first_category_id))

            body = [{
                'id'      : m_menu[0],
                m_menu[1] : [{
                    'id'      : f_menu[0],
                    f_menu[1] : [{
                        'id'   : s_menu[0],
                        'name' : s_menu[1]
                    } for s_menu in second_category if s_menu[2] == f_menu[0]]
                } for f_menu in first_category if f_menu[2] == m_menu[0]]
            } for m_menu in main_category]

            return jsonify(body), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()

    @product_app.route('', methods = ['GET'])
    @validate_params(
        Param('limit', GET, int, default = 100, required = False),
        Param('offset', GET, int, required = False),
        Param('main_category_id', GET, int, required = False),
        Param('first_category_id', GET, int, required = False),
        Param('second_category_id', GET, int, required = False),
        Param('is_promotion', GET, int, rules = [Enum(0, 1)], required = False),
        Param('select', GET, int, rules = [Enum(0, 1)], required = False),
        Param('q', GET, str, required = False)
    )
    def products(*args):
        """ 상품 정보 전달 API
        여러 상품 정보가 필요한 페이지에서 쿼리 파라미터로 필터링에 사용될 값을 받아 필터링된 상품의 데이터들을 표출합니다.

        returns :
            200: 상품 리스트
            500:

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-23 (고지원): 파라미터 유효성 검사
            2020-09-24 (고지원): 검색을 위한 파라미터 추가, 검색 시 셀러 리스트 추가
        """
        try:
            session = Session()
            # pagination
            filter_dict = {}
            filter_dict['limit'] = args[0]
            filter_dict['offset'] = args[1]

            # 카테고리
            filter_dict['main_category_id'] = args[2]
            filter_dict['first_category_id'] = args[3]
            filter_dict['second_category_id'] = args[4]

            # 세일
            filter_dict['is_promotion'] = args[5]

            # 판매량순, 최신순
            filter_dict['select'] = args[6]

            # 검색 필터
            q = args[7]
            filter_dict['q'] = q

            body = {
                'products' : [],
                'sellers'  : []
            }

            # 상품 데이터
            products = [{
                'id'             : product.id,
                'name'           : product.name,
                'image'          : product.main_img,
                'price'          : product.price,
                'sales_amount'   : product.sales_amount,
                'discount_rate'  : product.discount_rate,
                'discount_price' : product.discount_price,
                'seller_name'    : product.korean_name
            } for product in product_service.get_products(filter_dict, session)]

            body['products'] = products

            # 검색 쿼리 파라미터가 들어올 경우 전달하는 셀러 정보
            if q:
                sellers = {
                    'count'      : [],
                    'seller_list': []
                }

                seller_list = [{
                    'id'     : seller.id,
                    'name'   : seller.korean_name,
                    'image'  : seller.image_url,
                    'url'    : seller.site_url,
                } for seller in product_service.get_sellers(q, session)]

                # 셀러 검색 결과 개수
                sellers['count'] = len(seller_list)
                # 셀러 데이터
                sellers['seller_list'] = seller_list

                body['sellers'] = sellers

            return jsonify(body), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()

    @product_app.route('/product/<int:product_id>', methods=['GET'])
    def product(product_id):
        """ 상품 상세 정보 전달 API
        path parameter 를 받아 한 상품의 상세 데이터를 표출합니다.

        returns :
            200: 상위 카테고리에 따른 하위 카테고리 리스트
            500:

        Authors:
            고지원

        History:
            2020-09-23 (고지원): 초기 생성
            2020-09-24 (고지원): seller 데이터를 한 번의 쿼리로 가지고 오도록 수정
        """
        try:
            session = Session()
            product = product_service.get_product(product_id, session)

            body = {
                'id'             : product['p_id'],
                'name'           : product['name'],
                'price'          : product['price'],
                'discount_rate'  : product['discount_rate'],
                'discount_price' : product['discount_price'],
                'image'          : product['images'],
                'color'          : product['colors'],
                'size'           : product['sizes'],
                'sales_amount'   : product['sales_amount'],
                'seller_name'    : product['korean_name'],
                'seller_url'     : product['site_url'],
            }
            return jsonify(body), 200

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            session.close()

    return product_app