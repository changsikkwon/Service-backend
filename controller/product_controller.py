from flask import jsonify, Blueprint
from flask_request_validator import (
    GET,
    Param,
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
            500: Exception

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-25 (고지원): 한 번의 쿼리로 3개의 카테고리 데이터를 전달하도록 수정
        """
        try:
            session = Session()

            # 메뉴 데이터
            category = product_service.get_menu(None, session)

            # 각 카테고리를 저장하기 위한 리스트
            second_category, first_category, main_category = [], [], []

            # JOIN 을 하며 생기는 중복을 제거하기 위해서 중복 체크 후 리스트에 저장
            for i in category:

                # (메인 카테고리의 id, 이름) 이 main_category 에 없을 경우 append
                if (i.m_id, i.main_category_name) not in main_category:
                    main_category.append((i.m_id, i.main_category_name))

                # (첫 번째 카테고리의 id, 이름, 이에 해당하는 메인 카테고리의 id) 가 first_category 에 없을 경우 append
                if (i.f_id, i.first_category_name, i.main_category_id) not in first_category:
                    first_category.append((i.f_id, i.first_category_name, i.main_category_id))

                # (두 번째 카테고리의 id, 이름, 이에 해당하는 첫 번째 카테고리의 id) 가 second_category 에 없을 경우 append
                second_category.append((i.s_id, i.second_category_name, i.first_category_id))

            # 카테고리의 계층 구조를 전달하기 위한 JSON 형식
            body = [{
                # 메인 카테고리의 id 와 이름
                'id'      : m_menu[0],
                m_menu[1] : [{
                    # 첫 번째 카테고리의 id 와 이름
                    'id'      : f_menu[0],
                    f_menu[1] : [{
                        # 두 번째 카테고리의 id 와 이름
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
        Param('main_category_id', GET, int, rules = [Enum(4, 5, 6)], required = False),
        Param('first_category_id', GET, int, required = False),
        Param('second_category_id', GET, int, required = False),
        Param('is_promotion', GET, int, rules = [Enum(0, 1)], required = False),
        Param('select', GET, int, rules = [Enum(0, 1)], required = False),
        Param('q', GET, str, required = False),
        Param('all_items', GET, int, rules = [Enum(1)], required=False)
    )
    def products(*args):
        """ 상품 정보 전달 API
        여러 상품 정보가 필요한 페이지에서 쿼리 파라미터로 필터링에 사용될 값을 받아 필터링된 상품의 데이터들을 표출합니다.

        args:
            *args:
                limit: pagination 을 위한 파라미터
                offset: pagination 을 위한 파라미터
                main_category_id: 메인 카테고리의 pk
                first_category_id: 첫 번째 카테고리의 pk
                second_category_id: 두 번째 카테고리의 pk
                is_promotion: 세일 여부를 판단하기 위한 파라미터
                select: 최신순, 판매량순을 판단하기 위한 파라미터
                q: 검색을 위한 파라미터
                all_items: 전체 상품 리스트를 전달할지 판단하기 위한 파라미터

        returns :
            200: 상품 리스트
            500: Exception

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-23 (고지원): 파라미터 유효성 검사
            2020-09-24 (고지원): 검색을 위한 파라미터 추가, 검색 시 셀러 리스트 추가
            2020-09-28 (고지원): 브랜드, 뷰티 메인에서 필요한 데이터를 위한 필터링 추가
            2020-10-02 (고지원): 브랜드, 뷰티 메인의 첫 번째 카테고리 상품 리스트 전달
        """
        try:
            session = Session()

            # args[2]: 메인 카테고리의 pk, args[8]: 전체 상품을 보여줄 지 판단하는 파라미터, args[3]: first 카테고리의 pk, args[4]: second 카테고리의 pk
            if args[2] == 5 or args[2] == 6 and not args[8] and not args[3] and not args[4]:

                # (5: 브랜드, 6: 뷰티) 특정 메인 카테고리 아이디 파라미터만 들어올 경우 베스트 상품, 추천 상품 데이터 등을 전달
                body = {
                    'best_items'        : [],
                    'brand_items'       : [],
                    'recommended_items' : [],
                    'category_items'    : []
                }

                # Best 상품 필터 - 해당하는 메인 카테고리의 상품 중 판매량 순 10개만 가져오기 위해 선언
                best_prod_filter = {
                    'main_category_id' : args[2],
                    'limit'            : 10,
                }
                best_products = product_service.get_products(best_prod_filter, session)

                # 추천 상품 필터 - 할인율 기준
                recommended_prod_filter = {
                    'main_category_id': args[2],
                    'limit': 30,
                    'discount_rate': 1
                }
                recommended_products = product_service.get_products(recommended_prod_filter, session)

                # 파라미터로 들어온 카테고리의 id (args[2]) 에 따라 특정 셀러를 지정하고 상품 5개만 가져오기 위해 선언,
                # 카테고리 id 에 해당하는 첫 번째 카테고리 아이디로 필터링된 상품 리스트를 가져오기 위해 선언
                if args[2] == 5:
                    # 브랜드 셀러
                    seller_id = 30

                    # 브랜드에 해당하는 첫 번째 카테고리 아이디
                    f_cat_list = (12, 13, 14, 15, 16, 17, 18)  # 12(아우터), 13(상의), 14(바지), 15(원피스), 16(스커트), 17(신발), 18(가방)

                else:
                    # 뷰티 셀러
                    seller_id = 359

                    # 뷰티에 해당하는 첫 번째 카테고리 아이디
                    f_cat_list = (23, 24, 25, 26, 27, 28)  # 23(스킨케어), 24(메이크업), 25(바디케어), 26(헤어케어), 27(향수), 28(미용소품)

                # 브랜드 상품 리스트 필터
                seller_filter = {
                    'main_category_id' : args[2],
                    'seller_id'        : seller_id
                }
                brand_products = product_service.get_products(seller_filter, session)

                # 첫 번째 카테고리 id 를 하나씩 파라미터로 넘겨 상품 데이터 5개씩 가져온다.
                for id in f_cat_list:

                    # 브랜드, 뷰티 메인 페이지에서 첫 번째 카테고리 상품 5개 씩 보여주기 위한 필터
                    f_category_filter = {
                        'first_category_id'   : id,
                        'limit'               : 5
                    }

                    # 카테고리 id 와 함께 상품 리스트를 반환한다.
                    f_cat = product_service.get_menu(id, session)
                    category_products = dict()
                    category_products['category_id'] = id
                    category_products['category_name'] = f_cat[0].first_category_name
                    category_products['products'] = product_service.get_products(f_category_filter, session)

                    body['category_items'].append(category_products)

                body['best_items'] = best_products
                body['brand_items'] = brand_products
                body['recommended_items'] = recommended_products

                return body

            # 필터링을 위한 딕셔너리
            filter_dict = dict()

            # pagination
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
            filter_dict['q'] = args[7]

            # 메인 카테고리의 모든 상품 필터
            filter_dict['all_items'] = args[8]

            body = {
                'products': [],
                'sellers': [],
            }

            # 상품 데이터
            body['products'] = product_service.get_products(filter_dict, session)

            # 검색어가 들어올 경우 전달하는 셀러 정보
            if filter_dict['q']:

                # 필터링된 셀러 리스트를 가져오기 위한 딕셔너리
                seller_info = {}

                seller_info['name'] = filter_dict['q']
                seller_info['limit'] = 100

                # 검색된 셀러 리스트의 JSON 형식
                sellers = {
                    'count'      : [],
                    'seller_list': []
                }

                # 검색어에 해당하는 셀러의 리스트
                seller_list = [{
                    'id'     : seller.id,
                    'name'   : seller.korean_name,
                    'image'  : seller.image_url,
                    'url'    : seller.site_url,
                } for seller in product_service.get_sellers(seller_info, session)]

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

        args:
            product_id: 상품의 pk

        returns :
            200: 상위 카테고리에 따른 하위 카테고리 리스트
            500: Exception

        Authors:
            고지원

        History:
            2020-09-23 (고지원): 초기 생성
            2020-09-24 (고지원): seller 데이터를 한 번의 쿼리로 가지고 오도록 수정
        """
        try:
            session = Session()

            # 상품 데이터
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

    @product_app.route('/sellers', methods=['GET'])
    @validate_params(
        Param('limit', GET, int, default = 100, required = False),
        Param('offset', GET, int, required = False),
        Param('main_category_id', GET, int, rules = [Enum(4, 5, 6)], required = False),
        Param('select', GET, int, rules = [Enum(0, 1)], default = 1),
    )
    def sellers(*args):
        """ 셀러 리스트 전달 API
        query parameter 를 받아 필터링된 셀러 리스트 데이터를 표출합니다.

        args:
            *args:
                limit: pagination 을 위한 limit
                offset: pagination 을 위한 offset
                main_category_id: 셀러 속성을 필터링 하기 위한 파라미터
                select: 1 일 경우 판매량 순, 0 일 경우 최신 순으로 필터링

        returns :
            200: 셀러 리스트
            500: Exception

        Authors:
            고지원

        History:
            2020-09-30 (고지원): 초기 생성
        """
        try:
            session = Session()

            # 필터링을 위한 딕셔너리
            seller_dict = {}
            seller_dict['limit'] = args[0]
            seller_dict['offset'] = args[1]
            seller_dict['main_category_id'] = args[2]
            seller_dict['select'] = args[3]

            # 셀러 데이터
            sellers = product_service.get_sellers(seller_dict, session)

            body = [{
                'id'        : seller['id'],
                'name'      : seller['korean_name'],
                'image_url' : seller['image_url'],
                'site_url'  : seller['site_url'],
            } for seller in sellers]

            return jsonify(body), 200

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            session.close()

    return product_app