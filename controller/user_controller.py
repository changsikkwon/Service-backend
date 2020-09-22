import requests

from flask      import request, Blueprint, jsonify

def create_user_endpoints(user_service, Session):
    # Blueprint 설정
    user_app = Blueprint('user_app', __name__, url_prefix='/api/user')
    
    # 구글로그인
    @user_app.route("/google-login", methods = ['POST'], endpoint = 'google_login')
    def google_login():
        try:
            session = Session()
            
            google_token  = request.json['access_token']
            user_info     = requests.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    headers = {
                        "Authorization" : f"Bearer {google_token}"
                    }).json()
            
            login_user = user_service.get_or_create_google_user(
                {
                    "email"    : user_info['email'],
                    "name"     : user_info['name'],
                    "login_id" : user_info['sub']
                }, session)
            
            session.commit()
            
            if login_user:
                access_token = user_service.generate_access_token(login_user)
                return jsonify({'access_token' : access_token}), 200
        
        except Exception as e:
            session.rollback()
            return jsonify({'ERROR_MSG' : f'{e}'}), 500
        
        finally:
            session.close()
        
    return user_app