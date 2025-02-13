from app import create_app
from app.database import init_db

app = create_app()

init_db()

@app.route('/')
def hello_world():  # todo put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
