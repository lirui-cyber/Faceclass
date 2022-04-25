#coding:utf-8
import dlib

from scipy.spatial import distance
from face_recognition import *

import numpy as np

import time
import cv2


class Face_detector():
    def __init__(self,):

        self.face_detector = dlib.get_frontal_face_detector()
        #特征点检测
        self.ldmark_detector = dlib.shape_predictor('./dlib_model/shape_predictor_68_face_landmarks.dat')
        self.face_info = {}

        self.detecting = True  # flag of if detect face
        self.ldmarking = False  # flag of if detect landmark
        self.total = 0
        self.ear = 0

    def detect_face(self, img):
        if self.detecting:
            # print("img{0}".format(img))

            self.face_info = {}
            self.EYE_AR_CONSEC_FRAMES = 2
            self.frame_counter = 0;
            #det_start_time = time.time()
            dets = self.face_detector(img, 1) #dlib检测的特征点存到dets
            #print 'Detection took %s seconds.' % (time.time() - det_start_time)


            #print('Number of face detected: {}'.format(len(dets)))
            # if len(dets) > 0:
            #     self.textBrowser.append('Number of face detected: {}'.format(len(dets)))

            for k, d in enumerate(dets):
                #print("Detection {}: left: {} Top: {} Right: {} Bottom: {}".format(
                #    k, d.left(), d.top(), d.right(), d.bottom()
                #))
                #self.textBrowser.append("Detection {}: left: {} Top: {} Right: {} Bottom: {}".format(
                #    k, d.left(), d.top(), d.right(), d.bottom()))

                # ldmark detection
                landmarks = []
                shape = self.ldmark_detector(img, d)
                landmarks2 = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
                if self.ldmarking:
                    landmarks = landmarks2
                eye_l = landmarks2[36:42]
                eye_r = landmarks2[42:48]
                # print('eye_l = {0}'.format(eye_l))
                # print('eye_r = {0}'.format(eye_r))
                leftEAR = eye_aspect_ratio(eye_l)  # 计算左眼EAR
                rightEAR = eye_aspect_ratio(eye_r)  # 计算右眼EAR
                #print('leftEAR = {0}'.format(leftEAR))
                #print('rightEAR = {0}'.format(rightEAR))
                ear = (leftEAR + rightEAR) / 2.0  # 求左右眼EAR的均值



                 # 在图像上显示出眨眼次数blink_counter和EAR
                # cv2.putText(img, "Blinks:{0}".format(blink_counter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                #                     (0, 0, 255), 2)
                # cv2.putText(img, "EAR:{:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                #                     (0, 0, 255), 2)
                    #self.textBrowser.append('eye_l {}:{}'.format(eye_l[0], eye_r[1]))
                crop_face = np.copy(img[max(0, d.top()):d.bottom(), max(0,d.left()):d.right(), :])

                #print crop_face.shape
                #print ('top , bottom, left, right = {}, {}, {}, {}'.format(d.top(), d.bottom(), d.left(), d.right()))

                #save crop face
                #cv2.imwrite('./db/{}.jpg'.format(self.total), crop_face.copy())
                self.total+=1

                self.face_info[k] = ([d.left(), d.top(), d.right(), d.bottom()], landmarks[18:], crop_face)    # 0:18 are face counture
                #print('face_info::{0}'.format(self.face_info))
            # emit signal when detection finished
            # print "+++++++++++++++++++++{0}".format(img)
            face_recognition = Face_recognizer()
            pred, cord, label = face_recognition.face_recognition(self.face_info)
            return pred, cord, label
            # self.emit(QtCore.SIGNAL('yy(PyQt_PyObject)'))

    def detect_eye(self, img):
        if self.detecting:
            # print("img{0}".format(img))

            self.face_info = {}
            self.EYE_AR_CONSEC_FRAMES = 2
            self.frame_counter = 0;
            # det_start_time = time.time()
            dets = self.face_detector(img, 1)  # dlib检测的特征点存到dets
            # print 'Detection took %s seconds.' % (time.time() - det_start_time)

            # print('Number of face detected: {}'.format(len(dets)))
            # if len(dets) > 0:
            #     self.textBrowser.append('Number of face detected: {}'.format(len(dets)))

            for k, d in enumerate(dets):
                # print("Detection {}: left: {} Top: {} Right: {} Bottom: {}".format(
                #    k, d.left(), d.top(), d.right(), d.bottom()
                # ))
                # self.textBrowser.append("Detection {}: left: {} Top: {} Right: {} Bottom: {}".format(
                #    k, d.left(), d.top(), d.right(), d.bottom()))

                # ldmark detection
                landmarks = []
                shape = self.ldmark_detector(img, d)
                landmarks2 = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
                if self.ldmarking:
                    landmarks = landmarks2
                eye_l = landmarks2[36:42]
                eye_r = landmarks2[42:48]
                # print('eye_l = {0}'.format(eye_l))
                # print('eye_r = {0}'.format(eye_r))
                leftEAR = eye_aspect_ratio(eye_l)  # 计算左眼EAR
                rightEAR = eye_aspect_ratio(eye_r)  # 计算右眼EAR
                # print('leftEAR = {0}'.format(leftEAR))
                # print('rightEAR = {0}'.format(rightEAR))
                self.ear = (leftEAR + rightEAR) / 2.0  # 求左右眼EAR的均值

                # 在图像上显示出眨眼次数blink_counter和EAR
                # cv2.putText(img, "Blinks:{0}".format(blink_counter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                #                     (0, 0, 255), 2)
                # cv2.putText(img, "EAR:{:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                #                     (0, 0, 255), 2)
                # self.textBrowser.append('eye_l {}:{}'.format(eye_l[0], eye_r[1]))
                crop_face = np.copy(img[max(0, d.top()):d.bottom(), max(0, d.left()):d.right(), :])

                # print crop_face.shape
                # print ('top , bottom, left, right = {}, {}, {}, {}'.format(d.top(), d.bottom(), d.left(), d.right()))

                # save crop face
                # cv2.imwrite('./db/{}.jpg'.format(self.total), crop_face.copy())

        return self.ear
def eye_aspect_ratio(eye):

    #print(eye)
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear









