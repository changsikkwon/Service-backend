from .user_controller    import create_user_endpoints
from .product_controller import create_product_endpoints
from .qna_controller     import create_qna_endpoints
from .order_controller   import create_order_endpoints
from .review_controller  import create_review_endpoints
from .event_controller   import create_event_endpoints

__all__ = [
    'create_user_endpoints',
    'create_product_endpoints',
    'create_qna_endpoints',
    'create_order_endpoints',
    'create_review_endpoints',
    'create_event_endpoints'
]