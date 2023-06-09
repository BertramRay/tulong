#!/usr/local/bin/python3
from flask import Flask
# from flask_cors import CORS
from flask_restful import Api
from config import config
from resources.parser import ImageParser, Hello
from resources.uploader import ImageUploader
from resources.processor import ImageExtractor, ImageStyleDetector

app = Flask(__name__, static_folder='temp', )
Config = config["production"]
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# CORS(app,origins="*")

api = Api(app)

api.add_resource(ImageUploader, '/api/upload')
api.add_resource(ImageExtractor, '/api/extract')
api.add_resource(ImageStyleDetector, '/api/detect')
api.add_resource(ImageParser, '/api/parse')
api.add_resource(Hello, '/api/hello')


if __name__ == "__main__":
    print("hello")
    app.run(host='0.0.0.0')
