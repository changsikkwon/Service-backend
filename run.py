from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    app.run(host = '10.58.2.0', port = 5000, debug = True)