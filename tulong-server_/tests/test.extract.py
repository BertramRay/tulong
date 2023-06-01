from cv2 import cv2
import os
from tulong_api.core.extractor import TargetExtractor


def showImg(img):
    # return
    cv2.imshow("dialog", img)
    cv2.waitKey(0)


img, rects = TargetExtractor.extract(os.path.abspath(os.path.dirname(__file__)) + "/images/artboard.png", (24,1776,227,133))
for rect in rects:
    x, y, w, h = rect
    showImg(img[y:y + h, x:x + w])
# shapeDetector = ShapeDetector(image=res)
# shapeDetector.detect()

# cv2.imwrite('out.png',res)
