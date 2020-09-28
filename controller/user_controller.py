from util import login_required
import requests

from flask          import request, Blueprint, jsonify, g

from sqlalchemy     import exc

def create_user_endpoints(user_service, Session):
    # Blueprint 설정
    user_app = Blueprint('user_app', __name__, url_prefix='/api/user')
    
    @user_app.route("/googleLogin", methods = ['POST'], endpoint = 'google_login')
    def google_login():
        """ 구글로그인 로직
        구글유저 정보 요청 후 DB데이터 확인 후 토큰발행
        
        args :
            session : connection 형성된 session 객체
        
        returns :
            user access_token
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
        session = Session()
        try:
            google_token     = request.json['access_token']
            google_user_info = requests.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    headers  = {
                        "Authorization" : f"Bearer {google_token}"
                    }).json()
            check_user_info = {
                    "email" : google_user_info['email'],
                    "name"  : google_user_info['name'],
                }
            login_user = user_service.check_google_user(check_user_info, session)
            
            if login_user:
                dict_login_user = dict(login_user[0])
                access_token    = user_service.generate_access_token(dict_login_user['id'])
                
                return jsonify({'access_token' : access_token}), 200
                
            else:
                return jsonify({'message' : 'IVAILID_USER'}), 401
                        
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
        finally:
            session.close()
    
    @user_app.route("/googleSignup", methods = ['POST'], endpoint = 'google_sign_up')
    def google_sign_up():
        """ 구글신규유저 회원가입 로직
        구글 신규유저 회원가입 DB입력
        
        args :
            session : connection 형성된 session 객체
        
        returns :
            user access_token
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-26 (권창식) : 초기 생성
        """
        session = Session()
        try:            
            google_token     = request.json['access_token']
            google_user_info = requests.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    headers = {
                        "Authorization" : f"Bearer {google_token}"
                    }).json()
            
            sign_up_user_info = {
                'phone_number' : request.json['phone_number'],
                'login_id'     : request.json['login_id'],
                'email'        : google_user_info['email'],
                'name'         : google_user_info['name']
            }
              
            new_user_id  = user_service.google_sign_up_user(sign_up_user_info, session)
            access_token = user_service.generate_access_token(new_user_id)
            
            session.commit()
            return jsonify({'access_token' : access_token}), 200
        
        except exc.IntegrityError:
            return jsonify({'message' : 'DUPLICATE_DATA'}), 400
        
        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400
                    
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500    
        
        finally:
            session.close()
            
    @user_app.route("/shippingAddress/insert", methods = ['POST'], endpoint = 'insert_shipping_address')
    @login_required
    def insert_shipping_address():
        session = Session()
        try:
            shipping_address_info = request.json
            user_id               = g.user_id
            new_shipping_address  = user_service.insert_shipping_address(shipping_address_info, user_id, session)
            
            session.commit()
            return jsonify({'message' : new_shipping_address}), 200
        
        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400
        
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500

    @user_app.route("/shippingAddress/select", methods = ['GET'], endpoint = 'select_shipping_address')
    @login_required
    def select_shipping_address():
        session = Session()
        try:
            user_id               = g.user_id
            get_shipping_address  = user_service.select_shipping_address(user_id, session)
            shipping_address      = [dict(shipping_address) for shipping_address in get_shipping_address]
            return jsonify(shipping_address), 200

        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400
        
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
    @user_app.route("/shippingAddress/update", methods = ['POST'], endpoint = 'update_shipping_address')
    @login_required
    def update_shipping_address():
        session = Session()
        try:
            shipping_address_info   = request.json
            user_id                 = g.user_id
            user_service.update_shipping_address(shipping_address_info, user_id, session)
            
            session.commit()
            return jsonify({'message' : "SUCCESS"}), 200

        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400
        
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
        
    @user_app.route("/shippingAddress/delete", methods = ['DELETE'], endpoint = 'delete_shipping_address')
    @login_required
    def delete_shipping_address():
        session = Session()
        try:
            user_id     = g.user_id
            delete_info = request.json
            user_service.delete_shipping_address(user_id, delete_info, session)
            
            session.commit()
            return jsonify({'message' : 'SUCCESS'}), 200

        except KeyError:
            return jsonify({'message' : 'KEY_ERROR'}), 400
        
        except Exception as e:
            session.rollback()
            return jsonify({'message' : f'{e}'}), 500
    
    return user_app