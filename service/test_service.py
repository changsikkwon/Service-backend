class TestService:
    def __init__(self, test_dao):       
        self.test_dao = test_dao
        
    def get_text_in_test(self):
        return self.test_dao.get_text()