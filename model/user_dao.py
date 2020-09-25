from flask      import jsonify

class UserDao:        
    def insert_google_user(self, user_info, session):
        """구글유저 브랜디 회원가입 로직
                
        args :
            info_user : 구글에서 받아온 유저정보
        
        returns :
            회원가입 성공시 None
            실패시 에러발생
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
                
        row = session.execute(
            """ INSERT INTO users (
                email, 
                name,
                phone_number,
                login_id,
                platform_id,
                created_at,
                is_deleted
             )
             VALUES(
                :email,
                :sign_up_name,
                :phone_number,
                :login_id,
                2,
                now(),
                0
            )
            """
        ,
        ({'email' : user_info['email'], 'sign_up_name' : user_info['name'], 'phone_number' : user_info['phone_number'], 'login_id' : user_info['login_id']})).lastrowid
    
        return row
   
    def check_google_user(self, user_info, session):
        """
        구글유저 브랜디 회원 유무 파악 로직
                    
        args :
            info_user : 구글에서 받아온 유저정보
        
        returns :
            유저 있을 시 login_id return
            유저 없을 시 에러발생
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-24 (권창식) : 초기 생성
        """
    
        row = session.execute(
            """ SELECT email
                FROM users
                WHERE email = :email
            """
        ,{'email' : user_info['email']}).fetchall()
        
        return row