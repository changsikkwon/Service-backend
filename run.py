from app import create_app

if __name__ == '__main__':
    app = create_app()

    app.run(host = '10.251.1.153', port = 5000, debug = True)
