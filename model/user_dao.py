from flask      import jsonify

class UserDao:       
    def insert_google_user(self, user_info, session):
        try:
            user_email = user_info['email']
            user_name  = user_info['name']
            login_id   = user_info['login_id']
        
            row = session.execute(
                f"INSERT INTO users (name, email, login_id, platform_id, created_at, is_deleted) VALUES ('{user_name}', '{user_email}', '{login_id}', 2, now(), 0)").lastrowid
            
            return row

        except KeyError:
            return jsonify({'message': 'KEY_ERROR'}), 400
            
    def check_google_user(self, user_info, session):
        try:
            login_id = user_info['login_id']
            
            row = session.execute(
                f"SELECT login_id, platform_id FROM users WHERE login_id = '{login_id}' AND platform_id = 2").fetchone()
            return row
        
        except KeyError:
            return jsonify({'message': 'KEY_ERROR'}), 400