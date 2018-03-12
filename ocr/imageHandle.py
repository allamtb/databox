# encoding: utf-8
import numpy as np
import cv2
import collections
from matplotlib import gridspec
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import queue
import os

from tqdm import tqdm


class ImageHandler:
    '''
        如果type=url
        getimg參數要傳入requests回傳的content
        如果type=local
        getimg參數要傳入圖片本地路徑
        '''

    def __init__(self, getimg, type='url'):
        #  設置 matplotlib 中文字體
        self.cutStepNumber = 2
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
        #print(self.im.shape)
        self.im = cv2.dilate(self.im, (2, 2), iterations=1)
        rows,cols = self.im.shape
        for cols in range(cols):
            for row in range(rows):
                if self.im[row][cols] == 0:
                    count = 0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            try:
                                if self.im[row + k][cols + l] == 0:
                                    count += 1
                            except IndexError:
                                pass
                    # 這裡 threshold 設 4，當週遭小於 4 個點的話視為雜點
                    if count <= 7:
                        self.im[row][cols] = 255

        self.dicImg.update({"吹吹风": self.im.copy()})

    def RemoveNoiseLine(self):
        # 找出驗證碼干擾線的起點跟終點
        lineColor = 255  # 將線段設定為黑或白色 255:白 0:黑
        (rows, cols) = self.im.shape
        for col in range(cols):
            for row in range(rows):
                # 如果此點是黑点 往下找五個點
                if self.im[row][col] == 0:
                    count = 0
                    for c in range(row, row + 6):
                        try:
                            if self.im[c][col] == 0:
                                count += 1
                            else:
                                break
                        except:
                            pass
                    if count < self.cutStepNumber:
                        for c in range(0, count):
                            self.im[row + c][col] = lineColor  # 將此線段設為白色
                    row += self.cutStepNumber

        self.dicImg.update({"切切切": self.im.copy()})

    #  將圖片顯示出來
    def showImg(self, img=None):
        if img is None:
            img = self.im

        cv2.imshow(self.imageName, img)
        cv2.namedWindow(self.imageName, cv2.WINDOW_NORMAL)
        cv2.waitKey()

    def saveImg(self, filePath=None):

        cv2.imwrite(filePath, self.im)

    #  將多個圖片顯示在一個figure
    def saveImgEveryStep(self, raw_name, show=False):
        diclength = len(self.dicImg)
        if diclength > 0:
            fig = plt.figure(figsize=(10, 10))
            gs = gridspec.GridSpec(diclength + 1, 6)

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
            if show:
                plt.show()
            plt.savefig("../prethreatment/" + raw_name + ".jpg")
        else:
            print('圖片數字陣列為空')

    def findOnePoint(self, threshold):

        (rows, cols) = self.im.shape
        for col in range(cols):
            if col <= threshold:
                continue
            for row in range(rows):
                if self.im[row, col] == 0:
                    return (row, col)
        return None, None

    # 挖地雷的方法，一一打开未知领域。
    def findContinuousPoints(self, row_start, col_start):
        xaxis = []
        yaxis = []

        visited = set()
        q = queue.Queue()
        q.put((row_start, col_start))
        visited.add((row_start, col_start))
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # 四邻域
        diagoal = [ (-1,-1),(1,1),(-1,1),(1,-1)] # 对角邻域
        offsets.extend(diagoal)

        while not q.empty():
            x, y = q.get()

            for xoffset, yoffset in offsets:
                x_neighbor, y_neighbor = x + xoffset, y + yoffset

                if (x_neighbor, y_neighbor) in (visited):
                    continue  # 已经访问过了

                visited.add((x_neighbor, y_neighbor))

                try:
                    if self.im[x_neighbor, y_neighbor] == 0:
                        xaxis.append(x_neighbor)
                        yaxis.append(y_neighbor)
                        q.put((x_neighbor, y_neighbor))

                except IndexError:
                    pass
        if len(yaxis) == 0:
            return ([0],[0])

        return xaxis, yaxis

    def getLetterGroup(self):
        start = 0
        letterGroup = []
        while start < self.im.shape[1]:
            row_start_point, colum_Start_Point = self.findOnePoint(start)
            if row_start_point is None:
                break
            rows, cols = self.findContinuousPoints(row_start_point, colum_Start_Point)
            if (len(cols) > 200):
                letterGroup.append(cols)
            if max(cols) > start:
                start = max(cols)
            else:  # 其他情况（可能是遇到孤立的点），查找到的列的跨度+1
                start += 1
        return letterGroup

if __name__ == '__main__':
    path = "../data/captcha_dataset"
    for x in tqdm(os.listdir(path)):
        if os.path.isfile(os.path.join(path, x)):
            filePath = path + '\\' + x
            base_file_name = os.path.basename(filePath)
            raw_name, _ = os.path.splitext(base_file_name)
            imageHandler = ImageHandler(filePath, 'local')
            imageHandler.threshold()
            imageHandler.RemoveNoiseLine()
            imageHandler.removeNoise()
            imageHandler.saveImgEveryStep(raw_name)
            #imageHandler.saveImg("../prethreatment/" + raw_name + ".jpg")
            letterGroup= imageHandler.getLetterGroup()
            if len(letterGroup) != len(raw_name):
                # raise RuntimeError("验证码描述 {}和验证码切割长度{} 不匹配".format(raw_name, len(letterGroup)))
                print("验证码描述 {}和验证码切割长度{} 不匹配".format(raw_name, len(letterGroup)))
                continue
            for i in range(len(letterGroup)):
                letter_index = letterGroup[i]

                cropImage = imageHandler.im[:, min(letter_index):max(letter_index)]
                imageHandler.showImg(cropImage)
                cropImage= cv2.resize(cropImage, (20, 60))
                letterName = raw_name[i]
                directoryPath = '../data/sample/' + letterName
                if not os.path.exists(directoryPath):
                    os.makedirs(directoryPath)

                cv2.imwrite(directoryPath + "/" + letterName.upper() + "_" + raw_name + ".jpg", cropImage)
                cv2.waitKey(0)
