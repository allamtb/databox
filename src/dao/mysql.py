#!/usr/bin/python3
from datetime import datetime
import traceback

import pymysql


class mysql:
    def __init__(self):
        self.db = None
        self.cursor = None

    def checkConnect(self):
        if self.db is None:
            self.db = pymysql.connect("localhost", "root", "root", "databox")
        self.cursor = self.db.cursor()

    def showVersion(self):
        self.checkConnect()
        self.cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取单条数据.
        data = self.cursor.fetchone()
        print("Database version : %s " % data)

    def createTable(self):
        self.checkConnect()
        self.cursor.execute("DROP TABLE IF EXISTS `traindata`;")
        sql = """CREATE TABLE `traindata` (`captacha_name` varchar(20) NOT NULL,`captacha` blob NOT NULL,`sign` varchar(255) NOT NULL,
              `optdate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`captacha_name`),
              KEY `captacha` (`captacha_name`) USING BTREE
              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        print(sql)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except BaseException:
            # 如果发生错误则回滚
            traceback.print_exc()

            self.db.rollback()

    def addTrainData(self):
        self.checkConnect()
        # SQL 插入语句

        date = datetime.now().strftime("%Y-%m-%d %H")
        print(date)

        dt = datetime.strptime(date, "%Y-%m-%d %H")
        print(dt)
        sql = "INSERT INTO traindata(captacha_name,captacha,sign,optdate)VALUES" \
              " ('{}','{}', '{}', '{}')".format('2', '2', '3', str(date))
        print(sql)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except BaseException:
            # 如果发生错误则回滚
            traceback.print_exc()

            self.db.rollback()

    def closeDb(self):
        # 关闭数据库连接
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    m = mysql()
    m.createTable()
    m.addTrainData()
