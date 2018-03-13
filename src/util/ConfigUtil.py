from __future__ import unicode_literals
# -* - coding: UTF-8 -* -
import configparser
import os




def getConfig(section):
    work_dir = os.path.dirname(os.path.abspath(__file__))
    work_dir_upper = os.path.dirname(work_dir)
    work_dir_upper_upper = os.path.dirname(work_dir_upper)
    CONF_FILE = work_dir_upper_upper + os.path.sep + 'config' + os.path.sep + 'config.ini'

    config = configparser.ConfigParser()
    config.read(CONF_FILE, encoding='utf-8')
    return dict(config.items(section))


priceConfig = getConfig("price_line")


def getPriceConfig():
    return priceConfig


if __name__ == '__main__':
    print(os.getcwd())  # 获得当前工作目录
    getConfig("system")


sysConfig = getConfig("system")


def getSysConfig():
    return sysConfig

