#!/usr/local/bin/python3
from flask import Flask
# from flask_cors import CORS
from flask_restful import Api
from config import config
from resources.parser import ImageParser
from resources.uploader import ImageUploader
from resources.processor import ImageExtractor, ImageStyleDetector

app = Flask(__name__, static_folder='temp', )
Config = config["development"]
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# CORS(app,origins="*")

api = Api(app)

api.add_resource(ImageUploader, '/api/upload')
api.add_resource(ImageExtractor, '/api/extract')
api.add_resource(ImageStyleDetector, '/api/detect')
api.add_resource(ImageParser, '/api/parse')


@app.route('/')
def hello():
    return "<h1>" + "Hello World!" + "</h1>"


if __name__ == "__main__":
    app.run()
