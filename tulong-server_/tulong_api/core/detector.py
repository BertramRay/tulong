#!/usr/bin/env python3
import cv2
import numpy as np
import math
from .node import ShapeNode
from .utils import (
    single2three,
    image_morphology,
    image_contours,
    image_kmeansSegement,
    getMainColor,
    getCornerRadius,
    PHash,
    npbgra2rbgaList,
    npbgr2rgbList,
    showImg,
)

IMG_BORDER_WIDTH = 20
SCALE_SIZE = 1


class StyleDetector:
    def __init__(self, filePath="", image=None):
        _img = (
            image
            if type(image) is np.ndarray
            else cv2.imread(filePath, cv2.IMREAD_UNCHANGED)
        )
        con = np.where(_img[:, :, 3] == 0)
        _img[con[0], con[1], :] = 0
        showImg(_img)
        self.width = int(round(_img.shape[1] * SCALE_SIZE))
        self.height = int(round(_img.shape[0] * SCALE_SIZE))
        if SCALE_SIZE != 1:
            _img = cv2.resize(_img, (self.width, self.height))
        self._img = _img
        self.filePath = filePath
        # self.width = _img.shape[1]
        # self.height = _img.shape[0]
        img = cv2.copyMakeBorder(
            _img,
            IMG_BORDER_WIDTH,
            IMG_BORDER_WIDTH,
            IMG_BORDER_WIDTH,
            IMG_BORDER_WIDTH,
            cv2.BORDER_CONSTANT,
            value=[0, 0, 0, 0],
        )
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        showImg(gray)
        self.img = img
        self.gray = gray
        self._process()

    def _process(self):
        gray = self.gray
        img = cv2.Canny(gray, 50, 150)
        img = image_morphology(img)
        filled, stroked, cnts = image_contours(img)
        showImg(filled)
        # showImg(stroked)
        self.cnts = cnts
        self.filled = filled
        self.stroked = stroked

    def detect(self):
        isCircle = isRect = False
        width, height, x, y = getFrame(
            self.stroked, self.width, self.height, offest=IMG_BORDER_WIDTH
        )
        node = ShapeNode(width=width, height=height, x=x, y=y)
        print("宽:%d,高:%d,x:%d,y:%d" % (width, height, x, y))
        isCircle = self.detectCircle(node, self.filled)
        if isCircle:
            print("检测结果：圆形")
            node.shape = "circle"
            # node.width + node.height
            # node.width = node.height = radius * 2
            node.borderRadius = ["50%", "50%", "50%", "50%"]
        else:
            isRect, _width, _height = self.detectRectangle(node, self.filled)
            if _width is not None:
                if _width < width:
                    node.width = width
            if _height is not None:
                if _height < height:
                    node.height = height
            if isRect:
                print("矩形")
                node.shape = "rectangle"
                borderRadius = self.detectCorner(node)
                if borderRadius is None:
                    print("非规则形状")
                else:
                    node.borderRadius = list(map(restore, borderRadius))
            else:
                print("非规则形状")

        node.width = restore(node.width)
        node.height = restore(node.height)
        node.x = restore(node.x)
        node.y = restore(node.y)
        borderWidth, borderColor, contentMask = self.detectBorder(node)
        backgroundColor = self.detectBackground(node, contentMask)
        print("------最终结果------")
        print("宽:{},高:{},x:{},y:{}".format(node.width, node.height, node.x, node.y))
        print("圆角:{}".format(node.borderRadius))
        if borderColor:
            node.borderWidth = restore(borderWidth)
            node.borderColor = borderColor
            print("边框-厚度:{},边框-颜色:{}".format(borderWidth, borderColor))
        if backgroundColor:
            node.backgroundColor = backgroundColor
            print("背景色:{}".format(backgroundColor))

        node.imgWidth = self.width
        node.imgHeight = self.height
        return node

    # 形状检测
    def detectShape(self, node):
        pass

    # 检测圆形
    def detectCircle(self, node, img):
        draw_img = self.img.copy()
        circles = cv2.HoughCircles(
            img,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=30,
            param2=15,
            minRadius=10,
            maxRadius=0,
        )
        if circles is None:
            return False
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            _drawCircle(draw_img, i)
            # draw the outer circle
            rx = i[0] - IMG_BORDER_WIDTH
            ry = i[1] - IMG_BORDER_WIDTH
            return judgeCircle(i[2], rx, ry, node.width, node.height, node.x, node.y)
        return False

    # 检测矩形
    def detectRectangle(self, node, img):
        draw_img = self.img.copy()
        length_threshold = 10
        distance_threshold = 1.4

        canny_th1 = 50.0
        canny_th2 = 50.0
        canny_aperture_size = 3
        do_merge = True
        detector = cv2.ximgproc.createFastLineDetector(
            length_threshold,
            distance_threshold,
            canny_th1,
            canny_th2,
            canny_aperture_size,
            do_merge,
        )
        dlines = detector.detect(img)
        for [dline] in dlines:
            cv2.line(
                draw_img,
                (int(dline[0]), int(dline[1])),
                (int(dline[2]), int(dline[3])),
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )
        showImg(draw_img)
        lines = dlines.copy().reshape(dlines.shape[0], 4) - IMG_BORDER_WIDTH
        return judgeRectangle(lines, node.width, node.height)

    # 检测圆角
    def detectCorner(self, node):
        img = self._img
        target = img[node.y : node.y + node.height, node.x : node.x + node.width]
        showImg(target)
        half_width = int(node.width / 2)
        half_height = int(node.height / 2)
        lt_radius = getCornerRadius(target[:half_height, :half_width])
        rt_radius = getCornerRadius(target[:half_height, half_width:])
        rb_radius = getCornerRadius(target[half_height:, half_width:])
        lb_radius = getCornerRadius(target[half_height:, :half_width])

        borderRadius = [lt_radius, rt_radius, rb_radius, lb_radius]
        print("圆角:" + str(borderRadius))

        lt_vertify = vertifyCorner(target, lt_radius)
        rt_vertify = vertifyCorner(target, rt_radius)
        rb_vertify = vertifyCorner(target, rb_radius)
        lb_vertify = vertifyCorner(target, lb_radius)
        if lt_vertify & rt_vertify & rb_vertify & lb_vertify:
            # print("圆角:"+str(borderRadius))
            return borderRadius
        return None

    # 检测边框
    def detectBorder(self, node):
        labels, center = image_kmeansSegement(self.img)
        border = borderExtract(labels, center, self.filled)
        if border is None:
            return 0, None, self.filled
        scale, color, content_area = border
        border_width = node.width * scale
        border_color = npbgr2rgbList(color)
        return border_width, border_color, content_area

    def detectBackground(self, node, contentMask):
        img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        img = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=contentMask)
        # showImg(img)
        img_whitebg = img.copy()
        img_whitebg[contentMask == 0] = [255, 255, 255]

        # showImg(img_whitebg)
        background_color = backgroundColorExtract(img, contentMask, self.img)
        if background_color is None:
            background_color = backgroundColorExtract(
                img_whitebg, contentMask, self.img
            )
        if background_color is None:
            return background_color
        return npbgra2rbgaList(background_color)


def restore(val):
    if isinstance(val, str):
        return val
    return int(round(val / SCALE_SIZE))


def getFrame(img, originWidth=None, originHeight=None, offest=0):
    cntpos = np.where(img > 0)
    ypos = cntpos[0]
    xpos = cntpos[1]
    left = int(xpos.min() - offest)
    left = left if left > 0 else 0
    right = int(xpos.max() - offest)
    if originWidth is not None:
        if right > originWidth:
            right = originWidth
    top = int(ypos.min() - offest)
    top = top if top > 0 else 0
    bottom = int(ypos.max() - offest)
    if originWidth is not None:
        if right > originWidth:
            bottom = originHeight
    width = int(right - left)
    height = int(bottom - top)
    return width, height, left, top


# 判断是否为矩形
def judgeRectangle(lines, width, height, x=0, y=0):
    th = 2
    horizontal_segments = lines[np.where(abs(lines[:, 1] - lines[:, 3]) < th)]
    vertical_segments = lines[np.where(abs(lines[:, 0] - lines[:, 2]) < th)]
    isRect = False
    h = w = None
    if horizontal_segments.size != 0:
        horizontal_centers = (
            horizontal_segments[:, 1] / 2 + horizontal_segments[:, 3] / 2
        )
        top = horizontal_centers.min()
        bottom = horizontal_centers.max()
        h = bottom - top
        if abs(h - height) > th:
            return False, None, None  # 如果两线间隔非图形高度，则不规则图片
        isRect = True
        h = int(round(h))
    if vertical_segments.size != 0:
        vertical_centers = vertical_segments[:, 0] / 2 + vertical_segments[:, 2] / 2
        left = vertical_centers.min()
        right = vertical_centers.max()
        w = right - left
        if abs(w - width) > th:
            return False, None, None
        isRect = True
        w = int(round(w))
    return isRect, w, h


# 验证候选区域是否为圆角
def vertifyCorner(img, width):
    if width == 0:
        return True
    cornerArea = img[:width, :width]
    binary = np.zeros(cornerArea.shape[0:2], dtype=np.uint8)  # 构造二值图
    binary[cornerArea[:, :, 3] != 0] = 255
    horizontal = cv2.flip(binary, 1, dst=None)  # 水平镜像
    binary = cv2.hconcat([binary, horizontal])  # 水平拼接
    vertical = cv2.flip(binary, 0, dst=None)  # 垂直镜像
    img = cv2.vconcat([binary, vertical])  # 垂直拼接
    img = cv2.copyMakeBorder(
        img,
        IMG_BORDER_WIDTH,
        IMG_BORDER_WIDTH,
        IMG_BORDER_WIDTH,
        IMG_BORDER_WIDTH,
        cv2.BORDER_CONSTANT,
        value=[0],
    )
    # showImg(img)
    circles = cv2.HoughCircles(
        img, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=15, minRadius=10, maxRadius=0
    )
    if circles is None:
        return False
    else:
        return True


def judgeCircle(r, rx, ry, w, h, x=0, y=0, th=4):
    return (
        (abs(w - h) < th)
        & (abs(r - w / 2) < th)
        & (abs(rx - x - w / 2) < th)
        & (abs(ry - y - h / 2) < th)
    )


def borderExtract(labels, center, img_filled):
    for i in range(labels.max()):
        area = np.zeros((labels.size), dtype=np.uint8)
        area[labels == i] = 255
        area = area.reshape(img_filled.shape)
        # showImg(area)
        filled1, *_ = image_contours(area)
        result = filled1 - area
        result[result < 0] = 0
        filled2, *_ = image_contours(result)
        if isSimilar(filled1, filled2) & isSimilar(img_filled, filled1):
            s1 = np.where(filled1 > 0)[0].size
            s2 = np.where(filled2 > 0)[0].size
            scale = (1.0 - math.sqrt(s2 / s1)) * 0.5
            _drawBorder(filled1 - filled2, center[i])
            return scale, center[i], filled2
    return None


def backgroundColorExtract(img, img_filled, origin_img):
    labels, center = image_kmeansSegement(img)
    for i in range(labels.max()):
        area = np.zeros((labels.size), dtype=np.uint8)
        area[labels == i] = 255
        area = area.reshape(img_filled.shape)
        if isSimilar(area, img_filled, th=.88):
            color = getMainColor(origin_img[area > 0])
            _drawBackground(area, color)
            return color
    return None


# phash判断两图是否相似（缩放不变）
def isSimilar(img1, img2, th=0.8):
    HASH1 = PHash.pHash(img1)
    HASH2 = PHash.pHash(img2)
    distance, score = PHash.hammingDist(HASH1, HASH2)
    print(score)
    return score > th


def _drawCircle(draw_img, circle):
    cv2.circle(draw_img, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
    cv2.putText(
        draw_img,
        str(circle[2]),
        (circle[0], circle[1]),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
    )
    cv2.circle(draw_img, (circle[0], circle[1]), 2, (0, 0, 255), 3)

    print("半径:" + str(circle[2]))
    showImg(draw_img)


def _drawBorder(img, border_color):
    img[img < 0] = 0
    blank = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    blank[:, :] = border_color
    res = cv2.add(blank, np.zeros(np.shape(blank), dtype=np.uint8), mask=img)
    showImg(res)


def _drawBackground(img, color):
    res = single2three(img)
    res[img > 0] = color[:-1]
    showImg(res)


def _drawImgWithoutBorder(img, mask):
    res = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=mask)
    showImg(res)
