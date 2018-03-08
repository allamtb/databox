# encoding: utf-8
import numpy as np
import cv2
import collections
from matplotlib import gridspec
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import random, os

class Image:
    '''
        如果type=url
        getimg參數要傳入requests回傳的content
        如果type=local
        getimg參數要傳入圖片本地路徑
        '''

    def __init__(self, getimg, type='url'):
        #  設置 matplotlib 中文字體
        self.font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)
        #  儲存檔名
        self.imageName = 'fileName'
        # #  儲存路徑
        # self.Path = Path
        #  用來儲放分割後的圖片邊緣坐標(x,y,w,h)
        self.arr = []
        #  將每個階段做的圖存起來 用來debug
        self.dicImg = collections.OrderedDict()
        #  將圖片做灰階
        # self.im = cv2.imread(Path + "\\" + ImgName)
        if type == 'url':
            image = np.asarray(bytearray(getimg), dtype="uint8")
            self.im = cv2.imdecode(image, cv2.IMREAD_COLOR)
        elif type == 'local':
            self.im = cv2.imread(getimg)
            self.dicImg.update({"原始圖片": self.im.copy()})

        #  閾值化
    def threshold(self):
        # 115 是 threshold，越高濾掉越多
        # 255 是當你將 method 設為 THRESH_BINARY_INV 後，高於 threshold 要設定的顏色
        # 反轉黑白 以利輪廓識別
        gray_image = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        retval, self.im = cv2.threshold(gray_image, 115, 255, cv2.THRESH_BINARY)
        self.dicImg.update({"閾值化": self.im.copy()})

    #  去噪
    def removeNoise(self):
        # 先膨脹再去噪
        print(self.im.shape)
        self.im = cv2.dilate(self.im, (2, 2), iterations=1)
        print(self.im.shape)

        for i in range(len(self.im)):
            for j in range(len(self.im[i])):
                if self.im[i][j] == 0:
                    count = 0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            try:
                                if self.im[i + k][j + l] == 0:
                                    count += 1
                            except IndexError:
                                pass
                    # 這裡 threshold 設 4，當週遭小於 4 個點的話視為雜點
                    if count <= 12:
                        self.im[i][j] = 255

        self.dicImg.update({"去噪": self.im.copy()})



    def RemoveNoiseLine(self):
        # 找出驗證碼干擾線的起點跟終點
        lineColor = 222  # 將線段設定為黑或白色 255:白 0:黑
        (height, width) = self.im.shape
        for i in range(height):
            print('i=',i)
            # 搜尋最左邊pixel 如果此點是黑線 往下找五個點
            if self.im[i][0] == 0:
                count = 0
                for c in range(i, i+5):
                    try:
                        if self.im[c][0] == 0:
                            count += 1
                        else:
                            break
                    except:
                        pass
                if count >= 3:
                    for c in range(0,count):
                        print('i+c=', (i + c))
                        self.im[i + c][0] = lineColor # 將此線段設為白色
            # 搜尋最右邊pixel
            rightBorder = width-1
            if self.im[i][rightBorder] == 0:
                countRight = 0
                for c in range(i, i+5):
                    try:
                        if self.im[c][rightBorder] == 0:
                            countRight += 1
                        else:
                            break
                    except:
                        pass
                if countRight >= 3:
                    for c in range(0,countRight):
                        print('i+c=', (i + c))
                        self.im[i + c][rightBorder] = lineColor # 將此線段設為白色


        self.dicImg.update({"找出噪線": self.im.copy()})




    #  將圖片顯示出來
    def showImg(self, img=None):
        if img is None:
            img = self.im

        cv2.imshow(self.imageName, img)
        cv2.namedWindow(self.imageName, cv2.WINDOW_NORMAL)
        #  調整視窗 讓標題列顯示出來
        #cv2.resizeWindow(self.imageName, 250, 60)
        cv2.waitKey()
    #  將多個圖片顯示在一個figure
    def showImgEveryStep(self,):
        diclength = len(self.dicImg)
        if diclength > 0:
            fig = plt.figure(figsize=(10, 10))
            gs = gridspec.GridSpec(diclength+1, 6)

            # 依序列出dict物件裡的圖片
            for index, key in enumerate(self.dicImg):
                #  如果不是list物件 就是圖片 可以呼叫imshow
                if not isinstance(self.dicImg[key], list):
                    ax = fig.add_subplot(gs[index, :6])
                    ax.imshow(self.dicImg[key], interpolation='nearest')
                    ax.set_title(key, fontproperties=self.font)
                else:
                    try:
                        for i, img in enumerate(self.dicImg[key]):
                            ax = fig.add_subplot(gs[index, i])
                            ax.imshow(img, interpolation='nearest')
                    except IndexError:
                        pass

            plt.tight_layout()
            plt.show()
        else:
            print('圖片數字陣列為空')


if __name__ == '__main__':
    path = "../data/captcha_dataset"
    # 隨機選一張圖片

    for x in os.listdir(path):
        if os.path.isfile(os.path.join(path, x)):

            filename = path + '\\' + x
            print(filename)
            x = Image(filename, 'local')
            x.threshold()
            #x.RemoveNoiseLine()
            x.removeNoise()
           # x.showImgEveryStep()
            x.showImg()

            (height, width) = x.im.shape

