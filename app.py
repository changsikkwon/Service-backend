from flask                         import Flask
from flask_cors                    import CORS

from sqlalchemy                    import create_engine
from sqlalchemy.orm                import sessionmaker
from sqlalchemy.pool               import QueuePool
from model                         import ProductDao
from service                       import ProductService

from controller.product_controller import create_product_endpoints

def create_app(test_config = None):
    app = Flask(__name__)
    app.debug = True
    
    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)
        
    # DB 연결
    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', poolclass = QueuePool)
    Session = sessionmaker(bind = database)

    # CORS 설정
    CORS(app, resources = {r'*' : {'origins' : '*'}})
    
    # Persistance layer
    product_dao = ProductDao()
    
    # Business layer
    product_service = ProductService(product_dao)
    
    # Presentation layer
    app.register_blueprint(create_product_endpoints(product_service, Session))

    return app