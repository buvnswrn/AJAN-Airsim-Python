from flask import Flask
from flask_restx import Resource, Api
from apis import api
from constants.constants import FLASK_HOST, FLASK_PORT


app = Flask(__name__)
api.init_app(app)

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
