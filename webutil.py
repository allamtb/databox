import json
import requests
import time
import threading
from user_agent import generate_user_agent

pageSize = 20
request_id = int(time.time() * 1000)
# 稀有度倒序
RAREDEGREE_DESC = "RAREDEGREE_DESC"

# 稀有度正序
RAREDEGREE_ASC = "RAREDEGREE_ASC"

# 创建时间正序

CREATETIME_ASC = "CREATETIME_ASC"

#创建时间倒序

CREATETIME_DESC = "CREATETIME_DESC"




def get_headers():
    with open("data/headers.txt") as f:
        lines = f.readlines()
        headers = dict()
        for line in lines:
            splited = line.strip().split(":")
            key = splited[0].strip()
            value = ":".join(splited[1:]).strip()
            headers[key] = value
    return headers


_headers = get_headers()


def getMarketData(pageno=1):
    rawData = []
    try:
        data = {
            "appId": 1,
            "lastAmount": None,
            "lastRareDegree": None,
            "pageNo": pageno,
            "pageSize": pageSize,
            "petIds": [],
            "querySortType": "RAREDEGREE_DESC",
            "requestId": int(time.time() * 1000),
            "tpl": "",
        }


        myheader = _headers.copy()
        myheader['User-Agent']= generate_user_agent()

        page = requests.post("https://pet-chain.baidu.com/data/market/queryPetsOnSale", headers=myheader,
                             data=json.dumps(data))
        if page.json().get(u"errorMsg") == u"success":
            rawData = page.json()
    except Exception as e:
        print("Fault occur ！线程号{},处理页数{},异常内容{}".format(threading.currentThread().name, pageno,str(e)))
    return rawData


def getPetDetailByPetId(pet_no):
    rawData = []
    try:
        data = {
            "appId": 1,
            "petId": pet_no,
            "requestId": request_id,
            "tpl": ""
        }

        _headers[
            'Referer'] = "https://pet-chain.baidu.com/chain/detail?channel=market&petId={}&appId=1&validCode={}".format(
            pet_no, '')

        page = requests.post("https://pet-chain.baidu.com/data/pet/queryPetById", headers=_headers,
                             data=json.dumps(data))

        if page.json().get(u"errorMsg") == u"success":
            rawData = page.json().get(u"data").get(u"attributes")
    except Exception as e:
        print("Fault occur ！线程号{},处理狗狗ID{},异常内容{}".format(threading.currentThread().name, pet_no,str(e)))

    return rawData


def getTotalPages():
    total =getMarketData().get(u"data").get("totalCount")
    print("当前交易的莱茨狗总量{}个".format(total))
    return int(total / pageSize) + 1


def getPetsByPage(page_no):
    return getMarketData(page_no).get(u"data").get("petsOnSale")
