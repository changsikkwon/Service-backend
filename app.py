from flask                         import Flask
from flask_cors                    import CORS

from config                        import database
from sqlalchemy                    import create_engine

def create_app(test_config = None):
    app = Flask(__name__)
    
    # DB연결
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)
        
    database = create_engine(app.comfig['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database

    app.debug = True

#     # CORS 설정
    CORS(app, resources={r'*' : {'origins': '*'}})

    return app
