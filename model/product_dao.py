from flask import jsonify

from sqlalchemy import text

class ProductDao:
    def get_main_menu(self, session):
        try:
            row = session.execute(("""
                SELECT 
                    id, main_category_name
                FROM 
                    main_categories
            """))
            return row

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

    def get_first_menu(self, main_category_id, session):
        try:
            row = session.execute(("""
                SELECT 
                    id, first_category_name
                FROM 
                    first_categories
                WHERE 
                    main_category_id = :main_id
            """), {'main_id' : main_category_id})
            return row

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

    def get_second_menu(self, first_category_id, session):
        try:
            row = session.execute(("""
                SELECT 
                    id, second_category_name
                FROM 
                    second_categories
                WHERE 
                    first_category_id = :first_id
            """), {'first_id' : first_category_id})
            return row

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

    def get_seller_info(self, seller_id, session):
        try:
            row = session.execute(("""
                SELECT 
                    seller_id, korean_name
                FROM 
                    seller_info
                WHERE 
                    seller_id = :seller_id
            """), {'seller_id' : seller_id}).fetchone()
            return row

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

    def get_products(self, filter_dict, session):
        try:
            filter_query = """
                SELECT 
                    p.id, p_info.main_img, p_info.name, p_info.price, p_info.sales_amount, p_info.discount_rate, p_info.discount_price, p_info.seller_id
                FROM 
                    products AS p INNER JOIN product_info AS p_info ON p.id = p_info.product_id 
                WHERE 
                    p.is_deleted = 0 AND p_info.is_displayed = 1 
            """

            # first 카테고리
            if filter_dict.get('first_category_id', None):
                filter_query += " AND first_category_id = :first_category_id"

            # second 카테고리
            if filter_dict.get('second_category_id', None):
                filter_query += " AND second_category_id = :second_category_id"

            # 세일
            if filter_dict.get('is_promotion', None):
                filter_query += " AND p_info.is_promotion = :is_promotion"

            # 판매량, 최신순
            if filter_dict.get('select', None):
                filter_query += " ORDER BY p.created_at ASC"
            else:
                filter_query += " ORDER BY p_info.sales_amount DESC"

            # 페이징 시작
            if filter_dict.get('offset', None):
                filter_query += " OFFSET :offset"

            # 페이징 마지막
            if filter_dict.get('limit', None):
                filter_query += " LIMIT :limit"

            row = session.execute(text(filter_query), filter_dict)

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500
        return row