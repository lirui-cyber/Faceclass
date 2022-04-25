# coding=utf-8

from caffe_net import *
import glob
import caffe
import sklearn.metrics.pairwise
import cv2



class Face_recognizer():
    def __init__(self,):


        # load face model
        caffemodel = './deep_model/VGG_FACE.caffemodel'
        deploy_file = './deep_model/VGG_FACE_deploy.prototxt'
        mean_file = None
        self.net = Deep_net(caffemodel, deploy_file, mean_file, gpu=False)

        self.recognizing = True

        self.threshold = 40
        self.label = ['Stranger']
        self.db_path = './db'
        # self.db = []
        self.db = None
        # load db
        self.load_db()



    def load_db(self):
        if not os.path.exists(self.db_path):
            print('Database path is not existed!')
        folders = sorted(glob.glob(os.path.join(self.db_path, '*')))
        # 把每一个子文件夹的名字当做人的名字
        for name in folders:

            # print('loading {}:'.format(name))
            # 添加label
            self.label.append(os.path.basename(name))
            img_list = glob.glob(os.path.join(name, '*.jpg'))
            # print(img_list)
            # 针对每个人所有图都读进来
            imgs = [cv2.imread(img) for img in img_list]
            # print('imgs{0}'.format(imgs[0]))

            # 只使用feature
            scores, pred_labels, fea = self.net.classify(imgs, layer_name='fc7')

            # print('fea.shape {}'.format(fea.shape))

            # 取均值
            # print(fea[:])
            fea = np.mean(fea, 0)
            # print(fea[:])
            if self.db is None:
                self.db = fea.copy()
            else:
                self.db = np.vstack((self.db, fea.copy()))

            # print fea
            # print('done')
        #print self.label

    def face_recognition(self, face_info1):
        # print('face_info:\n')
        # print(face_info)
        face_info = [face_info1]
        if self.recognizing:
            img = []
            cord = []

            for k, face in face_info[0].items():
                # print 'k:{0}'.format(k)
                # print 'face:{0}'.format(face)
                # print('face[2]:{0}'.format(face[2]))
                face_norm = face[2].astype(float)
                face_norm = cv2.resize(face_norm, (128, 128))
                img.append(face_norm)
                cord.append(face[0][1:3])

            if len(img) != 0:
                # call deep learning for classfication
                prob, pred, fea = self.net.classify(img, layer_name='fc7')

                # print('fea_video{0}'.format(fea))
                # print('self.db{0}'.format(self.db))

                # search from db find the closest
                # fea是视频中的人或摄像头中的人  db是上一个函数得到的
                dist = sklearn.metrics.pairwise.cosine_similarity(fea, self.db)
                # print('dist = {0}'.format(dist))
                pred = np.argmax(dist, 1)
                dist = np.max(dist, 1)

                # print('pred = {0}'.format(pred))
                # print('maxdist = {0}'.format(dist))
                # print('threshold = {0}'.format(self.threshold/100.0))

                pred = [0 if dist[i] < self.threshold / 100.0 else pred[i] + 1 for i in range(len(dist))]

                # print('pred(after threshold) = {}'.format(pred))

                # writ on GUI

                # msg = QtCore.QString("Face Recognition Pred: <span style='color:red'>{}</span>".format(
                #     ' '.join([self.label[x] for x in pred])))
                # self.textBrowser.append(msg)
                # emit signal when detection finished
                # print('face_recognition_pred{0}'.format(pred))
                # print('face_recognition{0}'.format(cord))

                # 2018/8/31
                # for i in range(len(pred)):
                #     if pred[i] != 0:

                return pred, cord, self.label





