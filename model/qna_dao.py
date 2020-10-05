class QnaDao:
    def insert_question(self, qna_info, session):
        """ question 등록

        args:
            qna_info: question에 대한 정보
            session: 데이터베이스 session 객체

        Authors:
            고지원

        History:
            2020-09-26 (고지원): 초기 생성
        """
        session.execute(("""
        INSERT INTO questions
        (
            type_id,
            user_id,
            product_id,
            content,
            is_private,
            created_at,
            is_deleted
        ) VALUES (
            :type_id,
            :user_id,
            :product_id,
            :content,
            :is_private,
            now(),
            0
        )"""), qna_info)

    def delete_question(self, question_info, session):
        """ question 삭제

        question_id 에 해당하는 문의의 is_deleted 컬럼을 1로 수정합니다.

        args:
            question_id: question 아이디
            session: 데이터베이스 session 객체

        Authors:
            고지원

        History:
            2020-09-28 (고지원): 초기 생성
            2020-10-05 (고지원): 삭제하려는 user id 와 문의를 한 user id 가 같은 경우에만 삭제하도록 수정
        """
        row = session.execute(("""
        UPDATE questions AS q
        INNER JOIN users AS u ON u.id = q.user_id
        SET q.is_deleted = 1
        WHERE q.id = :question_id 
        AND q.user_id = :user_id
        """), question_info)

        return row.rowcount

    def get_qnas(self, qna_info, session):
        """ question 리스트 전달

        args:
            products_id: 상품 id
            session: 데이터베이스 session 객체

        returns :
            200: question 리스트

        Authors:
            고지원

        History:
            2020-09-26 (고지원): 초기 생성
            2020-09-27 (고지원): 수정
                - qna_info 파라미터에 따라 필터링되도록 수정
                - answer 정보 함께 전달되도록 수정
            2020-10-05 (고지원): pagination 추가
        """
        qna_query = """
            SELECT
                q.id AS q_id, 
                q.content AS q_content, 
                q.is_private AS q_is_private,
                q.created_at AS q_created_at,
                q.is_answered,
                q_t.type_name,
                q.created_at AS q_created_at,
                u.login_id,
                a.id AS a_id,
                a.content AS a_content,
                a.is_private AS a_is_private,
                a.created_at AS a_created_at,
                s_info.korean_name
            FROM questions AS q
            
            # 문의 정보 조인
            INNER JOIN users AS u ON u.id = q.user_id
            INNER JOIN question_types AS q_t ON q_t.id = q.type_id 
            
            # 답변 정보 조인
            LEFT OUTER JOIN answers AS a ON a.id = q.id
            LEFT OUTER JOIN sellers AS s ON s.id = a.replier_id
            LEFT OUTER JOIN seller_info AS s_info ON s_info.seller_id = s.id
            
            WHERE q.is_deleted = 0
        """

        # 유저 아이디
        if qna_info.get('user_id', None):
            qna_query += " AND u.id = :user_id"

        # 상품 아이디
        if qna_info.get('product_id', None):
            qna_query += " AND q.product_id = :product_id"

        # 답변 여부
        if qna_info.get('is_answered', None):
            qna_query += " AND q.is_answered = :is_answered"

        # 최신순으로 정렬
        qna_query += " ORDER BY q.created_at DESC"

        # limit
        if qna_info.get('limit', None):
            qna_query += " LIMIT :limit"

        # offset
        if qna_info.get('offset', None):
            qna_query += " OFFSET :offset"

        row = session.execute(qna_query, qna_info)

        return row