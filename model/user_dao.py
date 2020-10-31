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
        query = """INSERT INTO users (
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
        row = session.execute(query,
        {
        'email'        : user_info['email'],
        'sign_up_name' : user_info['name'],
        'phone_number' : user_info['phone_number'],
        'login_id'     : user_info['login_id']
        }).lastrowid
    
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
        query = """ SELECT email, id
                    FROM users
                    WHERE email = :email
                """
        row = session.execute(query, {'email' : user_info['email']}).fetchall()
        
        return row
    
    def count_shipping_address(self, user_id, session):
        """배송지정보 count 로직
        유저의 신규 배송지정보 count
                    
        args :
            user_id : 데코레이터 g객체 user_id
        
        returns :
            유저의 배송지 정보 count return
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-06 (권창식) : 초기 생성
        """
        query = """ SELECT COUNT(*) AS count
                    FROM shipping_address
                    WHERE user_id = :user_id
                    AND is_deleted = 0
                """
        count_shipping_address = session.execute(query, {'user_id' : user_id['user_id']}).fetchone()
        
        return count_shipping_address[0]
    
    def check_is_default(self, user_id, check_info, session):
        """기본 배송지 여부 check 로직                    
        args :
            check_info : path 파라미터로 입력받은 id 값
            user_id : 데코레이터 g객체 user_id
        
        returns :
            last row id
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-10 (권창식) : 초기 생성
        """
        query = """ SELECT id
                    FROM shipping_address
                    WHERE user_id = :user_id
                    AND is_default = 1
                    AND id = :id
                """
        row = session.execute(query,
        {
            'user_id' : user_id['user_id'],
            'id'      : check_info
        }).fetchall()
        
        return row
    
    def update_is_default(self, user_id, session):
        """기본 배송지 update로직
           신규 기본 배송지가 수정될 시 기존 기본배송지 0으로 수정           
        args :
            user_id : 데코레이터 g객체 user_id
        
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-10 (권창식) : 초기 생성
        """
        query = """ UPDATE shipping_address
                    SET is_default = 0,
                        created_at = now()
                    WHERE user_id = :user_id
                    AND is_default = 1
                """
        session.execute(query, {'user_id' : user_id['user_id']})
        
    def new_is_default(self, user_id, session):
        """새로운 기본 배송지 update 로직
           기존 기본 배송지가 삭제될 시 가장 최근에 생성된 기본 배송지가 기본 배송지로 변경
        args :
            user_id : 데코레이터 g객체 user_id

        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-10-10 (권창식) : 초기 생성
        """
        query = """ UPDATE shipping_address
                    SET is_default = 1,
                        created_at = now()
                    WHERE user_id = :user_id
                    AND is_default = 0
                    AND is_deleted = 0
                    ORDER BY created_at DESC LIMIT 1
                """
        session.execute(query, {'user_id' : user_id['user_id']})
    
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
            2020-10-06 (권창식) : is_default 추가
        """
        query = """INSERT INTO shipping_address (
                        user_id, 
                        zone_code,
                        address,
                        detail_address,
                        phone_number,
                        reciever,
                        is_default,
                        is_deleted,
                        created_at
                    )
                    VALUES(
                        :user_id,
                        :zone_code,
                        :address,
                        :detail_address,
                        :phone_number,
                        :reciever,
                        :is_default,
                        0,
                        now()
                )"""
        row = session.execute(query,       
        {
            'user_id'        : user_id['user_id'],
            'zone_code'      : shipping_address_info['zone_code'],
            'address'        : shipping_address_info['address'],
            'detail_address' : shipping_address_info['detail_address'],
            'phone_number'   : shipping_address_info['phone_number'],
            'reciever'       : shipping_address_info['reciever'],
            'is_default'     : shipping_address_info['is_default']
        }).lastrowid
        
        return row
    
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
        query = """ SELECT
                    id,
                    user_id,
                    zone_code,
                    address,
                    detail_address,
                    phone_number,
                    reciever,
                    is_default
                    FROM  shipping_address
                    WHERE user_id = :user_id
                    AND is_deleted = 0
                    ORDER BY is_default DESC
                """
        row = session.execute(query, {'user_id' : user_id['user_id']}).fetchall()
        
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
        query = """ UPDATE shipping_address
                    SET zone_code      = :zone_code,
                        address        = :address,
                        detail_address = :detail_address,
                        phone_number   = :phone_number,
                        reciever       = :reciever,
                        is_default     = :is_default,
                        created_at     = now()
                    WHERE id = :id
                    AND   user_id = :user_id
                """
        
        session.execute(query,
        {
            'user_id'        : user_id['user_id'],
            'zone_code'      : shipping_address_info['zone_code'],
            'address'        : shipping_address_info['address'],
            'detail_address' : shipping_address_info['detail_address'],
            'phone_number'   : shipping_address_info['phone_number'],
            'reciever'       : shipping_address_info['reciever'],
            'is_default'     : shipping_address_info['is_default'],
            'id'             : shipping_address_info['id']
        })
    
    def delete_shipping_address(self, user_id, delete_info, session):
        """배송지정보 delete 로직
        유저의 배송지정보 delete
                    
        args :
            delete_info : 삭제하고자 하는 배송지정보 id
            user_id     : 데코레이터 g객체 user_id
                
        Authors:
            kcs15987@gmail.com 권창식
        
        History:
            2020-09-28 (권창식) : 초기 생성
            2020-10-01 (권창식) : soft_delete로 변경
        """
        query = """ UPDATE shipping_address
                    SET is_deleted = 1,
                        created_at = now()
                    WHERE  id = :id
                    AND user_id = :user_id
                    AND is_deleted = 0
                """
        
        session.execute(query,
        {
            'user_id'    : user_id['user_id'],
            'id'         : delete_info
        })