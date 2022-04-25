#coding=utf-8
from flask import Flask, jsonify,request
import base64
import cv2
import time
import os
from FaceDetector import *
app = Flask(__name__)



@app.route('/face',methods=['POST'])
def get_frame():

    mc = request.form['images']
    upload_img = base64.b64decode(mc)
    nparr = np.fromstring(upload_img,np.uint8)
    img = cv2.imdecode(nparr,cv2.IMREAD_ANYCOLOR)
    face_detector = Face_detector()
    face_info = face_detector.detect_face(img)

    name_pred = face_info
    n_str = name_pred[0]
    # n_pos = name_pred[1]
    name_label = name_pred[2]
    name = name_label[n_str[0]]
    print("name_id:{0}".format(name))
    #
    return jsonify({'name': name})
    #return jsonify({'mc':mc})
    # upload_img = request.files['base']
    # print('base:'+ upload_img)
    # return 'sucess'
    # old_file_name = upload_img.filename
    # d= os.getcwd()
    # if upload_img:
    #      file_path= os.path.join(d,'static\img',old_file_name)
    #      upload_img.save(file_path)
    # else:
    #     return False
    #
    # img = cv2.imread("./static/img/" + old_file_name)
    #

    # print('old_file_name{0}'.format(old_file_name))


    # list = []
    # for i in range(len(n_str)):
    #
    #      list.append(name_label[n_str[i]])


@app.route('/faceeyecheck',methods=['POST'])
def get_faceeye():

    mc = request.form['images']
    upload_img = base64.b64decode(mc)
    nparr = np.fromstring(upload_img,np.uint8)
    img = cv2.imdecode(nparr,cv2.IMREAD_ANYCOLOR)

    face_detector = Face_detector()
    ear = face_detector.detect_eye(img)

    #
    return jsonify({'ear':ear})


if __name__ == '__main__':
    app.run(debug=True)
