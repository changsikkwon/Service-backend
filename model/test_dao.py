from sqlalchemy import text

class TestDao:
    def __init__(self, database):
        self.db = database

    def get_text(self):
        row = self.db.execute(text("""    
            SELECT
                id,
                text
            FROM test
        """)).fetchone()
        
        return {
            'id'   : row['id'],
            'text' : row['text']
        } if row else None