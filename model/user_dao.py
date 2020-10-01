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
        """INSERT INTO users (
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
        )"""
        ,({
        'email'        : user_info['email'],
        'sign_up_name' : user_info['name'],
        'phone_number' : user_info['phone_number'],
        'login_id'     : user_info['login_id']
        })).lastrowid
    
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
        """ SELECT email, id
            FROM users
            WHERE email = :email
        """
        , {'email' : user_info['email']}).fetchall()
        
        return row
    
    def insert_shipping_address(self, shipping_address_info, user_id, session):
        """배송지정보 insert 로직
        유저의 신규 배송지정보 insert
        해당 유저의 배송지 id가 5개 미만일 경우 insert
                    
        args :
            shipping_address_info : 유저가 입력한 배송지정보
            user_id : 데코레이터 g객체 user_id
        
        returns :
            insert 성공시 lastrowid
            배송지 정보가 5개 이상일 경우 None 
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
        """
        count_shipping_address = session.execute(
        """ SELECT id
            FROM shipping_address
            WHERE user_id = :user_id
        """
        ,{'user_id' : user_id['user_id']}).fetchall()
     
        if len(count_shipping_address) < 5:
            row = session.execute(
            """INSERT INTO shipping_address (
                    user_id, 
                    address,
                    phone_number,
                    reciever,
                    is_default
                )
                VALUES(
                    :user_id,
                    :address,
                    :phone_number,
                    :reciever,
                    0
            )"""
            ,({
                'user_id'      : user_id['user_id'],
                'address'      : shipping_address_info['address'],
                'phone_number' : shipping_address_info['phone_number'],
                'reciever'     : shipping_address_info['reciever'],
            })).lastrowid
            return row
        return None
    
    def select_shipping_address(self, user_id, session):
        """배송지정보 select 로직
        해당 유저의 모든 배송지 정보 select
                    
        args :
            user_id : 데코레이터 g객체 user_id
        
        returns :
            유저의 모든 배송지 정보
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
        """
        row = session.execute(
        """ SELECT
            id,
            user_id,
            address,
            phone_number,
            reciever,
            is_default
            FROM shipping_address
            WHERE user_id = :user_id
        """
        , {'user_id' : user_id['user_id']}).fetchall()
        
        return row

    def update_shipping_address(self, shipping_address_info, user_id, session):
        """배송지정보 update 로직
        유저의 배송지정보 update
                    
        args :
            shipping_address_info : 유저가 수정한 배송지정보
            user_id : 데코레이터 g객체 user_id
        
        returns :
            update 성공시 lastrowid
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
        """
        row = session.execute(
        """ UPDATE shipping_address
            SET address      = :address,
                phone_number = :phone_number,
                reciever     = :reciever,
                is_default   = :is_default
            WHERE id = :id
            AND   user_id = :user_id
        """
        ,{
            'address'      : shipping_address_info['address'],
            'phone_number' : shipping_address_info['phone_number'],
            'reciever'     : shipping_address_info['reciever'],
            'is_default'   : shipping_address_info['is_default'],
            'id'           : shipping_address_info['id'],
            'user_id'      : user_id['user_id']
        }).lastrowid
    
        return row
    
    def delete_shipping_address(self, user_id, delete_info, session):
        """배송지정보 delete 로직
        유저의 배송지정보 delete
                    
        args :
            delete_info : 삭제하고자 하는 배송지정보 id
            user_id : 데코레이터 g객체 user_id
                
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
        """
        session.execute(
        """ DELETE FROM shipping_address
            WHERE id = :id 
            AND   user_id = :user_id
        """
        ,{
            'user_id' : user_id['user_id'],
            'id'      : delete_info['id']
        })