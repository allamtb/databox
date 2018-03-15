import os
import random

import cv2
from dao.DataPrepareDao import DataPrepareDao
from datetime import datetime
import numpy as np
import base64


class DataPrepare:
    def __init__(self):

        self.dpDao = DataPrepareDao()

    def insertTrainData(self):

        # 列出data/sample/下面的所有数据

        date = datetime.now().strftime("%Y-%m-%d:%H")
        work_dir = os.path.dirname(os.path.abspath(__file__))
        work_dir_upper = os.path.dirname(work_dir)
        work_dir_upper_upper = os.path.dirname(work_dir_upper)
        # 目录结构/data/sample
        sampleDir = work_dir_upper_upper + os.path.sep + 'data' + os.path.sep + 'sample'
        listdir = os.listdir(sampleDir)
        # 遍历目录 /data/sample/2  ... 3 ... 4
        for imgSign in listdir:
            signDir = os.path.join(sampleDir, imgSign)
            # 得到图片地址 /data/sample/2/x_xxxx.jpg
            for imgFileName in os.listdir(signDir):
                imgFile = os.path.join(signDir, imgFileName)
                if os.path.isfile(imgFile):
                    imgData = cv2.imread(imgFile)
                    dumps = base64.b64encode(imgData.dumps())
                    # print(dumps)
                    # 依次插入到数据库的train表中
                    self.dpDao.addTrainData(imgFileName, dumps, imgSign, date)
        self.dpDao.closeDb()

    def getAllData(self):
        datas = self.dpDao.getTrainData()

        return datas

    def getTrainAndTestData(self):
        x_train = []
        y_train = []
        x_test = []
        y_test = []

        allData = list(self.getAllData())
        testSize = int(len(allData) / 10)

        random.shuffle(allData)
        testData = allData[:testSize]
        trainData = allData[testSize:]

        for test in testData:
            x_test.append(np.loads(base64.b64decode(test[1])))
            y_test.append(test[2])

        for train in trainData:
            x_train.append(np.loads(base64.b64decode(train[1])))
            y_train.append(train[2])

        return (np.array(x_train), np.array(y_train)), (np.array(x_test), np.array(y_test))


if __name__ == '__main__':
    dp = DataPrepare()
    dp.getTrainAndTestData()
    # for data in datas:
    #     data_ = data[0]
    #     mat = np.loads(base64.b64decode(data[1]))
    #     cv2.imshow(data_, mat)
    #     cv2.waitKey()
