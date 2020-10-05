class ReviewDao:
    def get_review(self, session, product_id):
        # Method: POST
        # data는 통신받은 메세지(dict 구조)
        # 주문을 해야 리뷰 작성 가능
        # 따라서 order_item_info id를 가져온다.
        querry = """
        SELECT
            rating,
            content,
            reviews.created_at,
            users.login_id,
            review_status.status_name
        FROM reviews

        INNER JOIN users
        ON reviews.user_id = users.id

        INNER JOIN review_status
        ON reviews.review_status_id = review_status.id
        
        INNER JOIN order_item_info
        ON reviews.order_item_info_id = order_item_info.id

        INNER JOIN products
        ON products.id = order_item_info.product_id

        WHERE products.id = :product_id
        """

        reviews = session.execute(querry, {"product_id": product_id}).fetchall()
        return reviews


    def insert_review(self, session, user_id, data):
        """ 리뷰 테이블에 데이터 삽입
        Method: POST
        
        args:
            session: 데이터베이스 session 객체
            data   : 
                args : rating(float), login_id(int), status_name(str), content(str)

        returns :
            200: Success

        Authors:
            문태기

        History:
            2020-10-03 (문태기): 초기 생성
        """

        querry_into_reviews = """
        INSERT INTO reviews(
            user_id,
            order_item_info_id,
            review_status_id,
            rating,
            content,
            created_at,
            is_deleted,
            product_id
        )
        VALUES(
            :user_id,
            :order_item_info_id,
            :review_status_id,
            :rating,
            :content,
            now(),
            0,
            :product_id
        )
        """

        # querry line
        session.execute(querry_into_reviews, {
            "user_id"           : user_id,
            "order_item_info_id": data["order_item_info_id"],
            "review_status_id"  : data["review_status_id"],
            "rating"            : data["rating"],
            "content"           : data["content"],
            "product_id"        : data["product_id"]
        })
