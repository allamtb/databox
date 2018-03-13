from __future__ import unicode_literals
# -* - coding: UTF-8 -* -
import configparser
import os




def getConfig(section):
    config = configparser.ConfigParser()
    config.read("../../config/config.ini", encoding='utf-8')
    return dict(config.items(section))


priceConfig = getConfig("price_line")


def getPriceConfig():
    return priceConfig


if __name__ == '__main__':
    print(os.getcwd())  # 获得当前工作目录


sysConfig = getConfig("system")


def getSysConfig():
    return sysConfig

