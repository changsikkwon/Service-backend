class QnaService:
    def __init__(self, qna_dao):
        self.qna_dao = qna_dao

    def insert_question(self, qna_info, session):
        """ question 작성

        사용자가 입력한 문의 데이터베이스에 입력합니다.

        Authors:
            고지원

        History:
            2020-09-26 (고지원): 초기 생성
        """
        self.qna_dao.insert_question(qna_info, session)

    def delete_question(self, question_id, session):
        """ question 삭제

        해당하는 문의를 삭제합니다.

        Authors:
            고지원

        History:
            2020-09-26 (고지원): 초기 생성
        """
        self.qna_dao.delete_question(question_id, session)

    def get_qnas(self, qna_info, session):
        """ question 리스트 전달

        qna_info 파라미터에 해당하는 상품의 question 리스트를 전달합니다.

        returns :
            200: question 리스트

        Authors:
            고지원

        History:
            2020-09-26 (고지원): 초기 생성
        """
        questions = self.qna_dao.get_qnas(qna_info, session)
        return questions