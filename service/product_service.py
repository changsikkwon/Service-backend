class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def get_main_menu(self, session):
        mains = self.product_dao.get_main_menu(session)
        return mains

    def get_first_menu(self, main_category_id, session):
        firsts = self.product_dao.get_first_menu(main_category_id, session)
        return firsts

    def get_second_menu(self, first_category_id, session):
        seconds = self.product_dao.get_second_menu(first_category_id, session)
        return seconds

    def get_seller_info(self, seller_id, session):
        seller = self.product_dao.get_seller_info(seller_id, session)
        return seller

    def get_products(self, filter_dict, session):
        products = self.product_dao.get_products(filter_dict, session)
        return products