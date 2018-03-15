import string

from util.RequestUtil import *
import datetime

import  numpy as np

def generateUserAgent():
    for i in range(100):
        print(generate_user_agent())


def generateCaptecha():
    for i in tqdm(range(200)):
        get_captcha()


class A:
    def __init__(self):
        self.time = "8:30"

    def foo(self, x):
        print("executing foo(%s,%s)" % (self, x))

    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))

    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)

    @property
    def showTime(self):
        return self.time

    @showTime.setter
    def showTime(self,time):
        self.time = time

def to_categorical(y, num_classes=None):
    """Converts a class vector (integers) to binary class matrix.

    E.g. for use with categorical_crossentropy.

    # Arguments
        y: class vector to be converted into a matrix
            (integers from 0 to num_classes).
        num_classes: total number of classes.

    # Returns
        A binary matrix representation of the input.
    """
    y = np.array(y).ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes))
    categorical[np.arange(n), y] = 1
    return categorical


if __name__ == '__main__':
    x = [1,1,1,1,1,2,3,4,5,6,7,8,8,9,2,3,5,9,4,'a']

    from sklearn.preprocessing import LabelBinarizer
    encoder = LabelBinarizer().fit(list(string.ascii_lowercase+'0123456789'))
    transform = encoder.transform(x)

    print(transform)

 #   print(string.ascii_lowercase)
    pass
    # a = A()
    # a.foo(1)
    # a.class_foo(1)
    # a.static_foo(1)
    # print(a.showTime)
    # a.showTime = "9:00"
    # print(a.showTime)
    # print(datetime.datetime.now().date())