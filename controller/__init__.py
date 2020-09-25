from .user_controller    import create_user_endpoints
from .product_controller import create_product_endpoints
from .qna_controller     import create_qna_endpoints

__all__ = [
    'create_user_endpoints',
    'create_product_endpoints',
    'create_qna_endpoints',
]