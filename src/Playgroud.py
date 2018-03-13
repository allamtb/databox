from util.RequestUtil import *
import datetime

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


if __name__ == '__main__':
    a = A()
    a.foo(1)
    a.class_foo(1)
    a.static_foo(1)
    print(a.showTime)
    a.showTime = "9:00"
    print(a.showTime)

    print(datetime.datetime.now().date())