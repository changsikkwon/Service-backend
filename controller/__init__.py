def create_endpoints(app, service):
    
    test_service  = service

    @app.route("/", methods=['GET'])
    def main():
        return test_service.get_text_in_test()