from flask import jsonify, Blueprint, request, g

from util  import login_required

def create_review_endpoints(review_services, Session):
    review_bp = Blueprint('review_app', __name__, url_prefix = '/api/review')

    @review_bp.route('', methods = ['GET'])
    def get_review_info():
        session    = Session()
        try:
            product_id = request.args.get('product_id')
            review_info = review_services.get_review(session, product_id)

            return jsonify({"result": [dict(row) for row in review_info]})

        except Exception as e:
            return jsonify({"ERROR": e}), 400
        
        finally:
            session.close()

    @review_bp.route('', methods = ['POST'])
    @login_required
    def insert_review_info():
        session = Session()
        try:
            data        = request.json
            user_id     = g.user_id["user_id"]
            review_services.insert_review(session, user_id, data)
            
            session.commit()
            return jsonify({"message": "SUCCESS"}), 200
        
        except Exception as e:
            session.rollback()
            return jsonify({"ERROR": e}), 400

        finally:
            session.close()

    return review_bp