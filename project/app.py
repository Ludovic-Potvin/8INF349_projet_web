from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # todo put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
