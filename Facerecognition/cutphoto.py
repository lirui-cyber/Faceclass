# -*- coding: UTF-8 -*-
"""
将指定目录下的所有图片的人脸抠出
"""
import dlib  # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2  # 图像处理的库OpenCv
import os

# dlib预测器
detector = dlib.get_frontal_face_detector()

# 读取图像的路径
path_read = './db/16/'

for file_name in os.listdir(path_read):
    # aa是图片的全路径
    aa = (path_read + "/" + file_name)
    # 读入的图片的路径中含非英文
    img = cv2.imdecode(np.fromfile(aa, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    # 获取图片的宽高
    img_shape = img.shape
    img_height = img_shape[0]
    img_width = img_shape[1]

    # 用来存储生成的单张人脸的路径
    path_save = './db/161102'

    # dlib检测
    dets = detector(img, 1)
    print("人脸数：", len(dets))

    for k, d in enumerate(dets):

        if len(dets) > 1:
            continue
        # 计算矩形大小
        # (x,y), (宽度width, 高度height)
        pos_start = tuple([d.left(), d.top()])
        pos_end = tuple([d.right(), d.bottom()])

        # 计算矩形框大小
        height = d.bottom() - d.top()
        width = d.right() - d.left()

        # 根据人脸大小生成空的图像
        img_blank = np.zeros((height, width, 3), np.uint8)

        for i in range(height):
            if d.top() + i >= img_height:  # 防止越界
                continue
            for j in range(width):
                if d.left() + j >= img_width:  # 防止越界
                    continue
                img_blank[i][j] = img[d.top() + i][d.left() + j]

        # cv2.imshow("face_"+str(k+1), img_blank)

        # 几种不同的插值方法
        # resize images to 200*200
        # temp=img_blank
        # img_blank = cv2.resize(img_blank, (200, 200), interpolation=cv2.INTER_NEAREST)
        # cv2.imencode('.jpg', img_blank)[1].tofile(path_save + "/"+"INTER_NEAREST" + file_name)  # 正确方法
        #
        # temp = img_blank
        # img_blank = cv2.resize(img_blank, (200, 200), interpolation=cv2.INTER_LINEAR)
        # cv2.imencode('.jpg', img_blank)[1].tofile(path_save + "/"  + "LINEAR"+file_name)  # 正确方法
        #
        # temp = img_blank
        # img_blank = cv2.resize(img_blank, (200, 200), interpolation=cv2.INTER_AREA)
        # cv2.imencode('.jpg', img_blank)[1].tofile(path_save + "/" + "INTER_AREA"+ file_name)  # 正确方法
        #
        # temp = img_blank
        # img_blank = cv2.resize(img_blank, (200, 200), interpolation=cv2.INTER_LANCZOS4)
        # cv2.imencode('.jpg', img_blank)[1].tofile(path_save + "/"  + "INTER_LANCZOS4"+ file_name)  # 正确方法

        img_blank = cv2.resize(img_blank, (200, 200), interpolation=cv2.INTER_CUBIC)

        # cv2.imwrite(path_save+"/"+file_name, img_blank)

        # cv2.imwrite("我//h.jpg", frame) #该方法不成功
        # cv2.imencode('.jpg', frame)[1].tofile('我/9.jpg') //正确方法
        # 保存图片路径有非中文字符
        cv2.imencode('.jpg', img_blank)[1].tofile(path_save + "/" + file_name)  # 正确方法
        # print(k)

        # cv2.waitKey(0)
