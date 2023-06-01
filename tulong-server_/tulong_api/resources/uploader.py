import werkzeug
import os
import time
import shutil
from flask_restful import Resource, reqparse
from flask import current_app
from utils.jwt_util import generate_token, verify_token
from utils.net import msgResponse


class ImageUploader(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location="cookies")
        parser.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location="files"
        )

        args = parser.parse_args()
        token = args["token"]
        img_file = args["file"]

        # 如果有，先清理
        if token:
            payload = verify_token(token, current_app.config["JWT_SECRET"])
            if payload:
                task_id = payload["task_id"]
                self.clearFile(task_id)

        task_id = self.generateTaskId()
        token = generate_token({"task_id": task_id}, current_app.config["JWT_SECRET"])
        url = self.saveFile(img_file, task_id)

        return msgResponse({"url": url}), 201, {"Set-Cookie": "token=" + token}

    def saveFile(self, f, task_id):
        # mimetype = '.' + f.mimetype.split('/')[-1]
        save_dir = current_app.config["UPLOAD_FOLDER"] + "/" + task_id
        os.mkdir(save_dir)
        file_name = "/{}/artboard.png".format(task_id)
        img_url = current_app.config["RESULT_URL"] + file_name
        img_path = current_app.config["UPLOAD_FOLDER"] + file_name
        f.save(img_path)
        return img_url

    def clearFile(self, task_id):
        file_dir = current_app.config["UPLOAD_FOLDER"] + "/" + task_id
        try:
            shutil.rmtree(file_dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def generateTaskId(self):
        return str(int(time.time()))
