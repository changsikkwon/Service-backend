import config

from flask                         import Flask
from flask_cors                    import CORS

from sqlalchemy                    import create_engine
from model                         import TestDao
from service                       import TestService
from controller                    import create_endpoints

def create_app(test_config = None):
    app = Flask(__name__)
    app.debug = True
    
    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)
        
    # DB 연결
    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)

    # CORS 설정
    CORS(app, resources={r'*' : {'origins': '*'}})
    
    # Persistance layer
    test_dao = TestDao(database)
    
    # Business layer
    test_service = TestService(test_dao)
    
    # Presentation layer
    create_endpoints(app, test_service)

    return app