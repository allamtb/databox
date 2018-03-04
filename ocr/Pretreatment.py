from PIL import Image
from RemoveNoiseLine import *
import numpy
from GetCropImages import *
from math import *
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
#step 1 灰度化




### No.4 二值化
def binarization(image):
    img_grey = image.convert('L')  # 灰度化

    threshold = 128  # 二值化阀值
    table = [] #二值化依据
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    img_bin = img_grey.point(table, '1')  # 二值化

    return img_bin

def removeNoise(image):
    width, height = image.size  # 获取宽和高

    is_once = False #是否继续去噪
    for x_column in range(width):
        for y_row in range(height):
            # 黑点周围黑点数（包括自己）少于3的 去掉黑点 设为白色
            if 0 < findIsolatedPoints(image, x_column, y_row) < 4:
                image.putpixel((x_column, y_row), 1)
                is_once = True

    return is_once, image#返回去噪声的图片

# 寻找孤立点 返回黑点8领域的黑点数量
def findIsolatedPoints(image, x_column, y_row):
    # 判断图片的长宽度下限
    cur_pixel = image.getpixel((x_column, y_row))  # 当前像素点的值
    width, height = image.size # 获取宽和高

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y_row == 0:  # 第一行
        if x_column == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel + image.getpixel((x_column, y_row + 1)) \
                  + image.getpixel((x_column + 1, y_row)) + image.getpixel((x_column + 1, y_row + 1))
            return 4 - sum
        elif x_column == width - 1:  # 右上顶点
            sum = cur_pixel  + image.getpixel((x_column, y_row + 1)) \
                  + image.getpixel((x_column - 1, y_row)) + image.getpixel((x_column - 1, y_row + 1))
            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = image.getpixel((x_column - 1, y_row)) + image.getpixel((x_column - 1, y_row + 1)) \
                  + cur_pixel + image.getpixel((x_column, y_row + 1)) \
                  + image.getpixel((x_column + 1, y_row)) + image.getpixel((x_column + 1, y_row + 1))
            return 6 - sum
    elif y_row == height - 1:  # 最下面一行
        if x_column == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel  + image.getpixel((x_column + 1, y_row)) \
                  + image.getpixel((x_column + 1, y_row - 1)) + image.getpixel((x_column, y_row - 1))
            return 4 - sum
        elif x_column == width - 1:  # 右下顶点
            sum = cur_pixel  + image.getpixel((x_column, y_row - 1)) \
                  + image.getpixel((x_column - 1, y_row)) + image.getpixel((x_column - 1, y_row - 1))
            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel  + image.getpixel((x_column - 1, y_row)) \
                  + image.getpixel((x_column + 1, y_row)) + image.getpixel((x_column, y_row - 1)) \
                  + image.getpixel((x_column - 1, y_row - 1)) + image.getpixel((x_column + 1, y_row - 1))
            return 6 - sum
    else:  # y不在边界
        if x_column == 0:  # 左边非顶点
            sum = image.getpixel((x_column, y_row - 1)) + cur_pixel \
                  + image.getpixel((x_column, y_row + 1)) + image.getpixel((x_column + 1, y_row - 1)) \
                  + image.getpixel((x_column + 1, y_row)) + image.getpixel((x_column + 1, y_row + 1))
            return 6 - sum
        elif x_column == width - 1:  # 右边非顶点
            sum = image.getpixel((x_column, y_row - 1)) + cur_pixel \
                  + image.getpixel((x_column, y_row + 1)) + image.getpixel((x_column - 1, y_row - 1)) \
                  + image.getpixel((x_column - 1, y_row)) + image.getpixel((x_column - 1, y_row + 1))
            return 6 - sum
        else:  # 具备9领域条件的
            sum = image.getpixel((x_column - 1, y_row - 1)) + image.getpixel((x_column - 1, y_row)) \
                  + image.getpixel((x_column - 1, y_row + 1)) + image.getpixel((x_column, y_row - 1)) \
                  + cur_pixel  + image.getpixel((x_column, y_row + 1)) + image.getpixel((x_column + 1, y_row - 1)) \
                  + image.getpixel((x_column + 1, y_row)) + image.getpixel((x_column + 1, y_row + 1))
            return 9 - sum

def startRefine(ori_image):
    img_grey = ori_image.convert('L')  # 灰度化

    threshold = 200  # 二值化阀值
    table = []  # 二值化依据
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    image = img_grey.point(table, '1')  # 二值化
    # image.show()

    # for x_row in range(height):
    #     for y_col in range(width):
    #         print(image_matrix[x_row][y_col], end=' ')
    #     print()
    count = 0
    while 1:
        removeNodules(image)
        count += 1

        if count == 20:
            break

    # print('count',count)
    return image

##细化图像 抽取骨架
def removeNodules(image):
    #事先做好的表
    array = [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
             1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
             0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
             1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
             1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
             1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, \
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
             0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
             1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
             0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
             1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
             1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
             1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
             1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, \
             1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]

    is_go = True # 是否继续
    w, h = image.size
    # 水平扫描
    next = 1
    for i in range(h):
        for j in range(w):
            if next == 0:
                next = 1
            else:
                m = image.getpixel((j - 1, i)) + image.getpixel((j + 1, i)) if 0 < j < w - 1 else 1
                if image.getpixel((j, i)) == 0 and m != 0:
                    a = [1] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and image.getpixel(
                                    (j - 1 + l, i - 1 + k)) == 0:
                                a[k * 3 + l] = 0
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image.putpixel((j, i), array[sum] * 255)
                    if array[sum] == 1:
                        is_go = False
                        next = 0

    # 竖直扫描
    next = 1
    for j in range(w):
        for i in range(h):
            if next == 0:
                next = 1
            else:
                m = image.getpixel((j, i - 1)) + image.getpixel((j, i + 1)) if 0 < i < h - 1 else 1
                if image.getpixel((j, i)) == 0 and m != 0:
                    a = [1] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and image.getpixel(
                                    (j - 1 + l, i - 1 + k)) == 0:
                                a[k * 3 + l] = 0
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image.putpixel((j, i), array[sum] * 255)
                    if array[sum] == 1:
                        is_go = False
                        next = 0

    # image.show()
    # image.save('r2.jpg')

    return is_go
#
# img_bin = binarization(img_grey)
#
# is_once = 1
# while is_once:
#     is_once, image_removedNoise = removeNoise(img_bin)  # No.5
#
#
# image_removedNoise.show()
#
# image_refined = startRefine(image_removedNoise)
#
# image_refined.show()



def imageZoom6020(image):
    image = image.convert('L')  # 灰度化
    width, height = image.size # 获取图像的宽和高
    zoom_k = min(width/60, height/20)# 缩放倍数
    # print('缩放倍数', zoom_k)

    # 缩放后的长宽
    new_w = int(width / zoom_k)
    new_h = int(height / zoom_k)
    # print("宽和高", new_w, " ", new_h)

    # 缩放后的新数组
    image_matrix = numpy.zeros([new_h, new_w])

    for x_column in range(new_w):
        for y_row in range(new_h):
            # 新图像坐标对应原图像的坐标
            x = x_column * zoom_k
            y = y_row * zoom_k
            #print(x, end=" ")
            #print(y)

            # 向下取整
            m = int(x)
            n = int(y)

            # 获取浮点数
            float_x = x - m
            float_y = y - n
            # print(float_x, end=" ")
            # print(float_y)

            # 边界判断
            if m+1 >= width:
                m = width-2
            if n+1 >= height:
                n = height-2

            # print(m, ' ', n)
            # print("4个点{},{},{},{}".format(image.getpixel((m,n)),image.getpixel((m,n+1)),image.getpixel((m+1,n)), image.getpixel((m+1,n+1))))
            first_n_pix = (image.getpixel((m,n+1))-image.getpixel((m,n))) * float_y + image.getpixel((m,n))
            second_n_pix = (image.getpixel((m+1, n+1)) - image.getpixel((m+1,n))) * float_y + image.getpixel((m+1,n))
            #print(int((second_n_pix - first_n_pix) * float_x + first_n_pix))
            image_matrix[y_row][x_column] = int((second_n_pix - first_n_pix) * float_x + first_n_pix)

    new_data = numpy.reshape(image_matrix,(new_h,new_w))
    #print(type(new_data))
    new_im = Image.fromarray(new_data)
    #new_im.show()## 显示图片

    return new_im

image = Image.open('../data/8tex.jpg')
image.show()
#img_grey = image.convert('L')  # 灰度化
image = imageZoom6020(image)# NO.O.2
### NO.3
image_refine = startRefine(image) #抽取骨架
remove_noise_line = RemoveNoiseLine(image_refine, image)
line_has, image_result = remove_noise_line.start()
image = binarization(image_result)# No.4
is_once, image = removeNoise(image)# No.5
while is_once:
    is_once, image = removeNoise(image)  # No.5
    # image.show()

##再次查找是否有干扰线 直到没有
while line_has:
    image_refine = startRefine(image)  # 抽取骨架
    remove_noise_line = RemoveNoiseLine(image_refine, image)
    line_has, image_result = remove_noise_line.start()
    image = binarization(image_result)  # No.4
    is_once, image = removeNoise(image)  # No.5
    # image.show()
    while is_once:
        is_once, image = removeNoise(image)  # No.5
        # image.show()
image.show()

image = beforCrop(image)  # 切割前处理

image.show()
# is_once, image = removeNoise(image)  # 去噪
# res_img_list = getCropImages(image)  # 切割
# same_img_list = []
# # 大小归一化
# for img in res_img_list:
#     width, height = img.size  # 获取图像的宽和高
#     # 删除异常图片
#     if width < 3 or height < 4:
#         continue
#
#     imageZoom6020(img).show()
#
