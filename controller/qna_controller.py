from flask import Blueprint, request, jsonify

from util import login_required

def create_qna_endpoints(qna_service, Session):

    qna_app = Blueprint('qna_app', __name__, url_prefix='/api/qnas')

    @qna_app.route('/qna', methods=['POST', 'DELETE'])
    # @login_required
    def qna():
        """ question 작성 API

        사용자가 입력한 문의를 데이터베이스에 입력합니다.

        returns :
            200: question 데이터베이스 입력
            400: KEY_ERROR
            500: Exception

        Authors:
            고지원

        History:
            2020-09-26 (고지원): 초기 생성
            2020-09-28 (고지원): delete 메소드 추가
        """
        try:
            session = Session()

            if request.method == 'POST':
                # 문의 입력을 위한 데이터를 받는다.
                qna_info = {
                    'type_id'    : request.json['type_id'],
                    'user_id'    : request.json['user_id'],
                    'product_id' : request.json['product_id'],
                    'content'    : request.json['content'],
                    'is_private' : request.json['is_private']
                }

                qna_service.insert_question(qna_info, session)

                session.commit()

                return jsonify({'message': 'INSERT_SUCCESS'}), 200

            # soft delete 를 위해 question_id 를 쿼리 파라미터로 받는다.
            question_id = request.args.get('question_id')
            qna_service.delete_question(question_id, session)

            session.commit()

            return jsonify({'message': 'DELETE_SUCCESS'}), 200

        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400

        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()

    @qna_app.route('', methods=['GET'])
    def qnas():
        """ QnA 리스트 전달 API

        user_id, product_id 에 따른 QnA 리스트를 표출합니다.

        returns :
            200: QnA 리스트
            500: Exception

        Authors:
            고지원

        History:
            2020-09-27 (고지원): 초기 생성
        """
        try:
            session = Session()

            # user 마이페이지에서는 데코레이터 엔드포인트 따로?
            qna_info = {}

            # 마이페이지 유저 아이디
            qna_info['user_id'] = request.args.get('user_id')

            # 상품 상세페이지 상품 아이디
            qna_info['product_id'] = request.args.get('product_id')

            # 답변 여부
            qna_info['is_answered'] = request.args.get('is_answered')

            body = [{
                'q_id'          : qna.q_id,
                'q_content'     : qna.q_content,
                'q_user'        : qna.login_id,
                'q_type'        : qna.type_name,
                'q_is_answered' : qna.is_answered,
                'q_is_private'  : qna.q_is_private,
                'a_id'          : qna.a_id,
                'a_content'     : qna.a_content,
                'a_is_private'  : qna.a_is_private,
                'a_created_at'  : qna.a_created_at
            } for qna in qna_service.get_qnas(qna_info, session)]

            return jsonify(body), 200

        except Exception as e:
            return jsonify({'message' : f'{e}'}), 500

        finally:
            session.close()

    return qna_app