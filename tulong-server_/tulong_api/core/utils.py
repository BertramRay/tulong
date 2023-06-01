import numpy as np
import math
import cv2
from itertools import chain


# 获取区域出现最多的颜色
def getMainColor(img):
    colors, count = np.unique(
        img.reshape(-1, img.shape[-1]), axis=0, return_counts=True
    )
    return colors[count.argmax()]


def getCornerRadius(target):
    cornerRadius = 0
    corner_mask_size = target[target[:, :, 3] < 1].size
    # corner_mask_size = node.width * node.height - target_size
    if corner_mask_size >= 0:
        cornerRadius = round(math.sqrt((corner_mask_size / 3) / (1 - np.pi / 4)))
    return cornerRadius


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))) * 360 / 2 / np.pi


# 二值图转三通道
def single2three(img):
    img_three = img.reshape((img.shape[0], img.shape[1], 1))
    img_three = np.concatenate((img_three, img_three, img_three), axis=-1)
    return img_three


def image_morphology(img, th=10, status=cv2.MORPH_CLOSE):
    # 建立一个椭圆核函数
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (th, th))
    # 执行图像形态学, 细节直接查文档，很简单
    closed = cv2.morphologyEx(img, status, kernel)
    return closed


def image_contours(img):
    cnts, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    size = img.shape[0], img.shape[1], 3
    bl1 = np.zeros(size, dtype=np.uint8)
    bl2 = np.zeros(size, dtype=np.uint8)
    filled = cv2.drawContours(bl1, cnts, -1, (255, 255, 255), thickness=cv2.FILLED)
    filled = cv2.cvtColor(bl1, cv2.COLOR_BGR2GRAY)
    stroked = cv2.drawContours(bl2, cnts, -1, (255, 255, 255), thickness=1)
    stroked = cv2.cvtColor(bl2, cv2.COLOR_BGR2GRAY)
    return filled, stroked, cnts


def image_kmeansSegement(img, k=10):
    # img = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    data = img.reshape((-1, 3))
    data = np.float32(data)

    # MAX_ITER最大迭代次数，EPS最高精度
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    num_clusters = k
    ret, label, center = cv2.kmeans(
        data, num_clusters, None, criteria, num_clusters, cv2.KMEANS_RANDOM_CENTERS
    )

    center = cv2.cvtColor(np.array([center], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0]
    labels = label.flatten()
    return labels, center


# 获取众数值
def getMode(ndarray):
    return np.argmax(np.bincount(ndarray))


def getFrame(img):
    cntpos = np.where(img > 0)
    ypos = cntpos[0]
    xpos = cntpos[1]
    if not ypos.size or not xpos.size:
        return None
    abX = int(xpos.min())
    abXops = int(xpos.max())
    abY = int(ypos.min())
    abYops = int(ypos.max())
    return abX, abY, abXops, abYops


class PHash(object):
    @staticmethod
    def pHash(img):
        """
        get image pHash value
        """
        # 加载并调整图片为32x32灰度图片
        img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)

        # 创建二维列表
        h, w = img.shape[:2]
        vis0 = np.zeros((h, w), np.float32)
        vis0[:h, :w] = img  # 填充数据

        # 二维Dct变换
        vis1 = cv2.dct(cv2.dct(vis0))
        # cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
        vis1.resize((32, 32), refcheck=False)

        # 把二维list变成一维list
        img_list = list(chain.from_iterable(vis1))

        # 计算均值
        avg = sum(img_list) * 1.0 / len(img_list)
        avg_list = ["0" if i < avg else "1" for i in img_list]

        # 得到哈希值
        return "".join(
            ["%x" % int("".join(avg_list[x : x + 4]), 2) for x in range(0, 32 * 32, 4)]
        )

    @staticmethod
    def hammingDist(s1, s2):
        """
        计算两张图片的汉明距离
        """
        assert len(s1) == len(s2)
        distance = sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])
        score = 1 - distance * 1.0 / (32 * 32 / 4)
        return distance, score


def npbgra2rbgaList(val):
    color = val[:-1][::-1].tolist()
    color.append(int(val[-1]))
    return color


def npbgr2rgbList(val):
    color = val[::-1].tolist()
    return color


def showImg(img):
    return
    cv2.imshow("dialog", img)
    cv2.waitKey(0)
