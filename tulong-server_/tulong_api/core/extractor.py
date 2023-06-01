#!/usr/bin/env python3
import cv2
import numpy as np
from .utils import showImg, getFrame, image_morphology


class TargetExtractor(object):
    @staticmethod
    def extract(filePath, in_rect):
        origin_img = cv2.imread(filePath)
        x, y, w, h = in_rect
        img = origin_img[y:y + h, x:x + w]

        # 获取目标近似位置作为前景区域
        pos = _getTargetPos(img)
        if not pos:
            return None, None

        sx, sy, ex, ey = pos
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (sx, sy, ex - sx, ey - sy)
        # 函数的返回值是更新的 mask, bgdModel, fgdModel
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 4, cv2.GC_INIT_WITH_RECT)
        mask = np.where((mask == 2) | (mask == 0), 0, 255).astype("uint8")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        # 羽化边缘
        new_mask = _smoothEdge(mask)
        img[:, :, -1] = new_mask
        con = np.where(img[:, :, -1] == 0)
        img[con[0], con[1], :] = 0

        boxes = _separate(new_mask)
        showImg(img)
        return img, boxes
        # 裁剪区域
        # abX, abY, abXops, abYops = getFrame(new_mask)
        # new_img = img[abY:abYops + 1, abX:abXops + 1]
        # return new_img, (abX, abY, abXops + 1, abYops + 1)


def _getTargetPos(img):
    """获取目标边界"""
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    img = cv2.Canny(img, 50, 150)
    # img = image_morphology(img)
    # filled,*_ = image_contours(img)
    # showImg(img)
    return getFrame(img)


def _separate(img, th=5):
    """分割图片"""
    new_img = img.copy()
    showImg(new_img)
    new_img = cv2.Canny(new_img, 50, 150)
    new_img = image_morphology(new_img)
    cnts, _ = cv2.findContours(new_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    data = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if (w < th) | (h < th):
            continue
        data.append((x, y, w - 1, h - 1))
    return data


def _smoothEdge(img):
    """羽化边缘"""
    SCALE_SIZE = 3
    h, w = img.shape[:2]
    size = int(round(w * SCALE_SIZE)), int(round(h * SCALE_SIZE))
    img = cv2.resize(img, size)
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    new_img = cv2.GaussianBlur(img, (3, 3), 0)
    new_img = cv2.resize(new_img, (w, h))
    # showImg(new_img)
    return new_img
