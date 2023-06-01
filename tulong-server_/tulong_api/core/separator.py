#!/usr/bin/env python3
import cv2
import numpy as np
from .utils import image_morphology, showImg
SCALE_SIZE = 1
class TargetSeparator:
    def __init__(self,filePath):
        _img = cv2.imread(filePath,cv2.IMREAD_UNCHANGED)
        if _img.shape[-1] == 4:
            con = np.where(_img[:,:,3] == 0)
            _img[con[0],con[1],:] = 0
        self.width = int(round(_img.shape[1] * SCALE_SIZE))
        self.height = int(round(_img.shape[0] * SCALE_SIZE))
        _img = cv2.resize(_img,(self.width,self.height))
        self.img = _img
    def separate(self,th=20):
        img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img,(3,3),0)
        # showImg(img)
        img = cv2.Canny(img,50,130)
        showImg(img)
        img = image_morphology(img,th)
        showImg(img)
        data = image_contours(img,self.img)
        # drawBox(data,img.shape[0:2])
        return data
    
def image_contours(img,draw_img):
    contours, _ = cv2.findContours(
        img.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
    data = []
    for i in range(len(contours)):
        cnt = contours[i]
        x, y, w, h = cv2.boundingRect(cnt)
        data.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h
        })
        img = cv2.rectangle(draw_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    showImg(img)
    return data

def drawBox(data, shape):
    img = np.zeros((shape[0],shape[1],3),dtype=np.uint8)
    boxes = []
    for i in range(len(data)):
        v = data[i]
        box = Box(abX=v["x"],abY=v["y"],abXops=v["x"]+v["w"],abYops=v["y"]+v["h"])
        boxes.append(box)
        img = cv2.rectangle(img, (box.abX, box.abY), (box.abXops, box.abYops), (255,255,255), -1)
    showImg(img)
    lines = []
    rootBox = Box(0,0,int(shape[1] - 1),int(shape[0] - 1))
    separateArea(boxes,rootBox,1,lines)
    img = drawBoxesLines(lines,img)
    # cv2.imwrite('t2_.png', img) 
    showImg(img)

def separateArea(boxes, parentBox, direction, lines): # 栅格化
    if len(boxes) <= 1: return
    # 按方向合并
    groups = mergeBoxes(boxes,direction)
    
    groupBoxes = [getGroupBox(group) for group in groups]
    addBoxesLines(groupBoxes,parentBox,direction,lines)
    # showImg(drawimg)
    for idx, group in enumerate(groups):
        separateArea(group, groupBoxes[idx],direction * -1, lines)

def getGroupBox(boxes):
    if len(boxes) == 1: return boxes[0]
    abX = min(box.abX for box in boxes)
    abY = min(box.abY for box in boxes)
    abXops = max(box.abXops for box in boxes)
    abYops = max(box.abYops for box in boxes)
    return Box(abX,abY,abXops,abYops)
    
def mergeBoxes(boxes, direction): # 成行或成列逻辑
    groups = []
    boxesLen = len(boxes)
    for box in boxes: box.groupIndex = -1

    for i in range(boxesLen - 1):
        boxA = boxes[i]
        for j in range(i + 1,boxesLen):
            boxB = boxes[j]
            if (boxA.groupIndex >= 0) & (boxA.groupIndex == boxB.groupIndex): continue # 排除同组元素
            if needMerge(boxA,boxB,direction): # 是否合并
                if (boxA.groupIndex < 0) & (boxB.groupIndex < 0):
                    groups.append([boxA,boxB])
                    boxA.groupIndex = boxB.groupIndex = len(groups) - 1
                elif (boxA.groupIndex >= 0) & (boxB.groupIndex >= 0):
                    groups[boxA.groupIndex] = (groups[boxA.groupIndex] + groups[boxB.groupIndex])
                    boxB_groupIndex = boxB.groupIndex
                    for b in groups[boxB.groupIndex]: b.groupIndex = boxA.groupIndex
                    groups[boxB_groupIndex] = []
                else:
                    if boxA.groupIndex >= 0:
                        groups[boxA.groupIndex].append(boxB)
                        boxB.groupIndex = boxA.groupIndex
                    else:
                        groups[boxB.groupIndex].append(boxA)
                        boxA.groupIndex = boxB.groupIndex
        if boxA.groupIndex < 0: groups.append([boxA])
    if boxes[-1].groupIndex < 0: groups.append([boxes[-1]]) # 最后一个元素判断
    groups = list(filter(lambda g: len(g) > 0, groups))
    for box in boxes: box.groupIndex = -1
    return groups

def needMerge(boxA, boxB, direction):
    if direction > 0: # 横向合并
        return not ((boxA.abY > boxB.abYops) | (boxA.abYops < boxB.abY))
    else: # 竖向合并
        return not ((boxA.abX > boxB.abXops) | (boxA.abXops < boxB.abX))

def addBoxesLines(boxes,parentBox, direction, lines):
    # drawimg = img.copy()
    for box in boxes:
        if direction > 0: # 横线
            lines.append([parentBox.abX,box.abY,parentBox.abXops,box.abY])
            lines.append([parentBox.abX,box.abYops,parentBox.abXops,box.abYops])
        else: # 竖线
            lines.append([box.abX,parentBox.abY,box.abX,parentBox.abYops])
            lines.append([box.abXops,parentBox.abY,box.abXops,parentBox.abYops])

def drawBoxesLines(lines,drawimg):
    for line in lines:
        drawimg = cv2.line(drawimg,(line[0],line[1]),(line[2],line[3]),color = (255,255,0),thickness=1)
        showImg(drawimg)
    return drawimg


class Box:
    def __init__(self,abX = 0,abY = 0,abXops = 0,abYops = 0):
        self.id = str(abX) + str(abY) + str(abXops) + str(abYops)
        self.abX = abX
        self.abY = abY
        self.abXops = abXops
        self.abYops = abYops