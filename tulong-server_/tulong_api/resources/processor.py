import cv2
from flask_restful import Resource, reqparse
from flask import current_app
from utils.jwt_util import verify_token
from core.extractor import TargetExtractor
from core.detector import StyleDetector
from utils.net import msgResponse


class ImageExtractor(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location="cookies")
        parser.add_argument(
            "frame",
            type=dict,
            required=True,
            location="json",
            help="frame cannot be blank!",
        )
        args = parser.parse_args()
        token = args["token"]
        frame = args["frame"]
        payload = getPayload(token)
        if payload:
            task_id = payload["task_id"]
            out_rects_data = self.extract(task_id, frame)
            out_rects_data = [] if not out_rects_data else out_rects_data
            return msgResponse({"out_rects": out_rects_data})
        else:
            return invalidTaskResponse()

    def extract(self, task_id, in_rect_data):
        task_dir = "{}/{}/".format(current_app.config["UPLOAD_FOLDER"], task_id)
        task_url = "{}/{}/".format(current_app.config["RESULT_URL"], task_id)
        in_path = task_dir + "artboard.png"
        in_rect = (
            int(in_rect_data["x"]),
            int(in_rect_data["y"]),
            int(in_rect_data["w"]),
            int(in_rect_data["h"]),
        )
        out_img, out_rects = TargetExtractor.extract(in_path, in_rect)
        if out_img is None:
            return None

        out_rects_data = []
        for out_rect in out_rects:
            out_rect_data = {}
            x, y, w, h = out_rect
            out_rect_data["x"] = x + in_rect[0]
            out_rect_data["y"] = y + in_rect[1]
            out_rect_data["w"] = w
            out_rect_data["h"] = h
            out_rect_id = generateRectId(out_rect_data["x"], out_rect_data["y"], w, h)
            out_rect_data["id"] = out_rect_data["name"] = out_rect_id
            out_rect_data["url"] = task_url + out_rect_id + ".png"

            out_rect_path = task_dir + out_rect_id + ".png"
            cv2.imwrite(out_rect_path, out_img[y : y + h, x : x + w])
            out_rects_data.append(out_rect_data)

        return out_rects_data


class ImageStyleDetector(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location="cookies")
        parser.add_argument(
            "img_id",
            type=str,
            required=True,
            location="json",
            help="img_id cannot be blank!",
        )
        args = parser.parse_args()
        token = args["token"]
        img_id = args["img_id"]
        payload = getPayload(token)
        if payload:
            task_id = payload["task_id"]
            style_data = self.detect(task_id, img_id)
            style_data = {} if not style_data else style_data
            return msgResponse({"style_data": style_data})
        else:
            return invalidTaskResponse()

    def detect(self, task_id, img_id):
        in_path = "{}/{}/{}.png".format(
            current_app.config["UPLOAD_FOLDER"], task_id, img_id
        )
        styleDetector = StyleDetector(in_path)
        styles = vars(styleDetector.detect())
        return styles


def generateRectId(x, y, w, h):
    return "{}_{}_{}_{}".format(x, y, w, h)


def getPayload(token):
    if token:
        payload = verify_token(token, current_app.config["JWT_SECRET"])
        return payload
    else:
        return False


def invalidTaskResponse():
    return msgResponse(code="10000", msg="task is invalid!")
