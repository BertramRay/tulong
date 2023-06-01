import cv2
import werkzeug
from flask_restful import Resource, reqparse
from flask import current_app
from utils.jwt_util import generate_token, verify_token
from utils.net import msgResponse
import resources.processor
from resources.processor import ImageExtractor, ImageStyleDetector
from resources.uploader import ImageUploader


def upload_image(f, token):
    # 如果有，先清理
    if token:
        payload = verify_token(token, current_app.config["JWT_SECRET"])
        if payload:
            task_id = payload["task_id"]
            ImageUploader.clearFile(ImageUploader, task_id)

    task_id = ImageUploader.generateTaskId(ImageUploader)
    token = generate_token({"task_id": task_id}, current_app.config["JWT_SECRET"])
    url = ImageUploader.saveFile(ImageUploader, f, task_id)
    return url, token, task_id


def extract_image(task_id, frame):
    return ImageExtractor.extract(ImageExtractor, task_id, frame)


def detect_UI_styles(task_id, image_id):
    return ImageStyleDetector.detect(ImageStyleDetector, task_id, image_id)


class ImageParser(Resource):
    def post(self):
        # upload image
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location="cookies")
        parser.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location="files"
        )
        args = parser.parse_args()
        token = args["token"]
        img_file = args["file"]
        url, token, task_id = upload_image(img_file, token)
        # extract image
        img_path = "{}/{}/".format(current_app.config["UPLOAD_FOLDER"], task_id) + "artboard.png"
        img = cv2.imread(img_path)
        height, width, _ = img.shape
        frame = {
            'x': 0,
            'y': 0,
            'w': width,
            'h': height
        }
        out_rects_data = extract_image(task_id, frame)
        # detect UI styles
        styles_data = []
        for out_rect_data in out_rects_data:
            styles = detect_UI_styles(task_id, out_rect_data['id'])
            styles_data.append(styles)
        return msgResponse({"styles_data": styles_data}), 201, {"Set-Cookie": "token=" + token}
