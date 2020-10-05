class ProductDao:
    def get_menu(self, first_category_id, session):
        """ 카테고리 데이터 전달
        
        args:
            session: 데이터베이스 session 객체

        returns :
            200: 메뉴 리스트

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-24 (고지원): 하나씩 존재했던 3개의 카테고리 정보를 가져오는 메소드를 JOIN 을 통해 한 번에 전달하도록 수정
            2020-10-03 (고지원): 첫 번째 카테고리 id 로 필터링 추가
        """
        filter_query = """
            SELECT
                m_cat.id AS m_id, 
                m_cat.main_category_name,
                f_cat.id AS f_id,
                f_cat.first_category_name,
                f_cat.main_category_id,
                s_cat.id AS s_id,
                s_cat.second_category_name,
                s_cat.first_category_id
            FROM main_categories AS m_cat 
            LEFT OUTER JOIN first_categories AS f_cat ON m_cat.id = f_cat.main_category_id
            LEFT OUTER JOIN second_categories AS s_cat ON f_cat.id = s_cat.first_category_id
        """

        # 첫 번째 메뉴의 id
        if first_category_id:
            filter_query += " WHERE f_cat.id = :first_id"

        row = session.execute(filter_query, {'first_id' : first_category_id}).fetchall()

        return row

    def get_sellers(self, seller_dict, session):
        """ 셀러 정보 리스트 전달

        args:
            seller_id: 셀러를 판단하기 위한 아이디
            session: 데이터베이스 session 객체

        returns :
            200: 셀러 리스트 정보

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-24 (고지원): 최근 데이터만 전달되도록 수정 및 이름 필터링을 위한 LIKE 절 추가
            2020-09-30 (고지원): 셀러 속성과 판매량, 최신순 필터 추가
        """
        filter_query = """
            SELECT
                s.id, 
                s_info.korean_name, 
                s_info.image_url,
                s_info.site_url,
                SUM(p_info.sales_amount) AS sales_amount
            FROM seller_info AS s_info
            
            # 셀러 테이블 조인 
            INNER JOIN sellers AS s ON s.id = s_info.seller_id
            
            # 셀러의 속성 정보 테이블 조인 
            INNER JOIN seller_attributes AS s_attr ON s_attr.id = s_info.seller_attribute_id
            
            # 상품 정보 테이블 조인
            LEFT OUTER JOIN product_info AS p_info ON p_info.seller_id = s.id
            
            WHERE s.is_deleted = 0
            AND s_info.end_date = '9999-12-31 23:59:59'
            AND p_info.is_deleted = 0
        """

        # 이름 검색어
        if seller_dict.get('name', None):

            # 이름 검색어를 formatting 하여 LIKE 절에 사용
            name = seller_dict['name']
            seller_dict['name'] = f'%{name}%'

            filter_query += " AND s_info.korean_name LIKE :name"

        # 쇼핑몰 / 브랜드 / 뷰티 셀러 필터링
        if seller_dict.get('main_category_id', None):
            filter_query += " AND s_attr.attribute_group_id = :main_category_id"

        # 셀러의 판매량을 COUNT 하기 위해
        filter_query += " GROUP BY s_info.seller_id"

        # 판매량순 / 최신순 필터링
        if seller_dict.get('select', None) == 0:
            filter_query += " ORDER BY s.created_at DESC"
        else:
            filter_query += " ORDER BY sales_amount DESC"

        # limit
        if seller_dict.get('limit', None):
            filter_query += " LIMIT :limit"

        # offset
        if seller_dict.get('offset', None):
            filter_query += " OFFSET :offset"

        row = session.execute(filter_query, seller_dict).fetchall()

        return row

    def get_products(self, filter_dict, session):
        """ 상품 리스트 표출

        쿼리 파라미터에 따른 필터링된 상품 리스트를 전달합니다.

        args:
            filter_dict: 필터링을 위한 딕셔너리
            session: 데이터베이스 session 객체

        returns :
            200: 필터링된 상품 리스트

        Authors:
            고지원

        History:
            2020-09-21 (고지원): 초기 생성
            2020-09-23 (고지원): created_at 컬럼을 통해 최신 이력 데이터만 나오도록 수정
            2020-09-24 (고지원): 이름 검색 필터 추가, is_deleted 컬럼을 통해 최신 이력 가져오도록 수정
            2020-09-28 (고지원): 브랜드, 할인율 필터 추가
        """
        filter_query = """
            SELECT 
                p.id, 
                p_info.main_img, 
                p_info.name, 
                p_info.price, 
                p_info.sales_amount, 
                p_info.is_promotion,
                p_info.discount_rate, 
                p_info.discount_price, 
                p_info.is_promotion,
                p_info.seller_id,
                s_info.korean_name,
                s_info.site_url,
                f_cat.first_category_name
            FROM products AS p
            
            # 상품 정보 조인
            INNER JOIN product_info AS p_info ON p.id = p_info.product_id
            
            # 셀러 정보 조인 
            INNER JOIN sellers AS s ON p_info.seller_id = s.id
            INNER JOIN seller_info AS s_info ON s_info.seller_id = s.id
            
            # 카테고리 정보 조인 
            INNER JOIN first_categories AS f_cat ON f_cat.id = first_category_id
            INNER JOIN main_categories AS m_cat ON m_cat.id = main_category_id
            
            WHERE p_info.is_deleted = 0 
            AND p.is_deleted = 0 
            AND p_info.is_displayed = 1
        """
        # main 카테고리
        if filter_dict.get('main_category_id', None):
            filter_query += " AND main_category_id = :main_category_id"

        # first 카테고리
        if filter_dict.get('first_category_id', None):
            filter_query += " AND first_category_id = :first_category_id"

        # second 카테고리
        if filter_dict.get('second_category_id', None):
            filter_query += " AND second_category_id = :second_category_id"

        # 세일
        if filter_dict.get('is_promotion', None) in (0, 1):
            filter_query += " AND p_info.is_promotion = :is_promotion"

        # 브랜드
        if filter_dict.get('seller_id', None):
            filter_query += " AND s.id = :seller_id"

        # 상품 이름 검색
        if filter_dict.get('q', None):
            q = filter_dict['q']
            filter_dict['q'] = f'%{q}%'
            filter_query += " AND p_info.name LIKE :q"

        # 판매량, 최신순
        if filter_dict.get('select', None):
            filter_query += " ORDER BY p.created_at DESC"
        else:
            filter_query += " ORDER BY p_info.sales_amount DESC"

        # pagination
        if filter_dict.get('limit', None):
            filter_query += " LIMIT :limit"

        # pagination
        if filter_dict.get('offset', None):
            filter_query += " OFFSET :offset"

        row = session.execute(filter_query, filter_dict)

        return row

    def get_product(self, product_id, session):
        """ 상품 상세 데이터 전달

        args:
            product_id: 해당하는 상품의 아이디
            session: 데이터베이스 session 객체

        returns :
            200: 상품 상세 정보

        Authors:
            고지원

        History:
            2020-09-23 (고지원): 초기 생성
            2020-09-24 (고지원): 셀러 테이블을 JOIN 하여 상품 데이터와 함께 셀러 데이터 가지고 오도록 수정
        """
        product_info = session.execute(("""
            SELECT 
                p.id AS p_id, 
                p_info.id AS p_info_id, 
                p_info.name, 
                p_info.price, 
                p_info.sales_amount, 
                p_info.discount_rate, 
                p_info.discount_price,
                p_info.seller_id,
                s_info.korean_name,
                s_info.site_url
            FROM products AS p 
            INNER JOIN product_info AS p_info ON p_info.product_id = :product_id
            INNER JOIN sellers AS s ON p_info.seller_id = s.id
            INNER JOIN seller_info AS s_info ON s_info.seller_id = s.id
            WHERE p.id = :product_id
            ORDER BY p_info.created_at DESC 
            LIMIT 1
        """), {'product_id' : product_id}).fetchone()

        # 컬러
        colors = session.execute(("""
            SELECT 
                id, 
                color_name
            FROM colors 
            WHERE product_info_id = :product_info_id
        """), {'product_info_id' : product_info.p_info_id})

        # 사이즈
        sizes = session.execute(("""
            SELECT 
                id, 
                size_name
            FROM sizes
            WHERE product_info_id = :product_info_id
        """), {'product_info_id' : product_info.p_info_id})

        # 이미지
        images = session.execute(("""
            SELECT 
                id, 
                URL
            FROM product_images
            WHERE product_info_id = :product_info_id
            ORDER BY ordering 
        """), {'product_info_id' : product_info.p_info_id})

        product_info = dict(product_info)

        color_list = [{
            "id": color.id, "color": color.color_name
        } for color in colors]
        product_info['colors'] = color_list

        size_list = [{
            "id": size.id, "size": size.size_name
        } for size in sizes]
        product_info['sizes'] = size_list

        image_list = [{
            "id": image.id, "image_url": image.URL
        } for image in images]
        product_info['images'] = image_list

        return product_info