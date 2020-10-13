from app import create_app

if __name__ == '__main__':
    app = create_app()

    app.run(host = '10.251.1.134', port = 5000, debug = True, threaded = True)