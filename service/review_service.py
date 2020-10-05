class ReviewService:
    # review_dao(DB와 직접 소통하는 1계층) 인스턴스를 저장
    def __init__(self, review_dao):
        self.review_dao = review_dao

    # 특정 상품에 달려있는 review들 보내주기
    def get_review(self, session, product_id):
        review_info = self.review_dao.get_review(session, product_id)
        return review_info

    # 특정 상품에 달리는 review들 db에 삽입하기
    def insert_review(self, session, user_id, data):
        response = self.review_dao.insert_review(session, user_id, data)
        return response
    