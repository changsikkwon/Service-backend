from flask import request, jsonify, Blueprint

def create_product_endpoints(product_service, Session):

    product_app = Blueprint('product_app', __name__, url_prefix='/products')

    @product_app.route('/category', methods = ['GET'])
    def product_category():
        """ 카테고리 정보 전달 API """
        try:
            session = Session()
            body = [{
                'id'                    : main.id,
                main.main_category_name : [{
                    'id'                     : first.id,
                    first.first_category_name: [{
                        'id'   : second.id,
                        'name' : second.second_category_name
                    }for second in product_service.get_second_menu(first.id, session)]
                }for first in product_service.get_first_menu(main.id, session)]
            }for main in product_service.get_main_menu(session)]
            return jsonify(body), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500
        finally:
            session.close()

    @product_app.route('', methods = ['GET'])
    def products():
        """ 상품 정보 전달 API """
        try:
            session = Session()
            # pagination
            filter_dict = {}
            filter_dict['limit'] = request.args.get('limit', 100, int)
            filter_dict['offset'] = request.args.get('offset', 0, int)

            # 카테고리
            filter_dict['first_category_id'] = request.args.get('first_category_id', None)
            filter_dict['second_category_id'] = request.args.get('second_category_id', None)

            # 세일
            filter_dict['is_promotion'] = request.args.get('is_promotion', False)

            # 판매량순, 최신순
            filter_dict['select'] = request.args.get('select', False)

            body = [{
                'id'             : product.id,
                'name'           : product.name,
                'image'          : product.main_img,
                'price'          : product.price,
                'sales_amount'   : product.sales_amount,
                'discount_rate'  : product.discount_rate,
                'discount_price' : product.discount_price,
                'seller_name'    : product_service.get_seller_info(product.seller_id, session).korean_name
            } for product in product_service.get_products(filter_dict, session)]
            print(jsonify(body))
            return jsonify(body), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500
        finally:
            session.close()

    return product_app