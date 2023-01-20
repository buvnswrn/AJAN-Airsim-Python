from flask import Flask
from flask_restx import Resource, Api
from apis import api
from constants.constants import FLASK_HOST, FLASK_PORT
import logging
import sys
logging.getLogger().addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api.init_app(app)

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
    app.logger.info("Starting AJAN Airsim Controller")
