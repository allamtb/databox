from __future__ import unicode_literals
import requests
import json
import time

pageSize = 20
request_id = int(time.time() * 1000)


def getMarketData(pageno=1):
    rawData = []
    try:
        data = {
            "appId": 1,
            "lastAmount": 1,
            "lastRareDegree": 0,
            "pageNo": pageno,
            "pageSize": pageSize,
            "petIds": [],
            "querySortType": "AMOUNT_ASC",
            "requestId": request_id,
            "tpl": "",
        }
        page = requests.post("https://pet-chain.baidu.com/data/market/queryPetsOnSale", headers=_headers,
                             data=json.dumps(data))
        if page.json().get(u"errorMsg") == u"success":
            rawData = page.json()
    except Exception as e:
        print(e)
    return rawData


def getPetDetailByNo(pet_no):
    rawData = []
    try:
        querypet_data = {
            "appId": 1,
            "petId": pet_no,
            "requestId": request_id,
            "tpl": ""
        }

        _headers[
            'Referer'] = "https://pet-chain.baidu.com/chain/detail?channel=market&petId={}&appId=1&validCode={}".format(
            pet_no, '')

        page = requests.post("https://pet-chain.baidu.com/data/pet/queryPetById", headers=_headers,
                             data=json.dumps(querypet_data))

        if page.json().get(u"errorMsg") == u"success":
            rawData = page.json().get(u"data").get(u"attributes")
    except Exception as e:
        print(e)

    return rawData


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


def getTotalPages():
    return int(getMarketData().get(u"data").get("totalCount") / pageSize) + 1


def getPetsByPage(page_no):
    return getMarketData(page_no).get(u"data").get("petsOnSale")




_headers = get_headers()
totalPageSize = getTotalPages()
all_Pets = []

# for i in range(1):
#     all_Pets.append(getPetsByPage(i + 1))
#
# with open("all_pets.json", 'w', encoding='utf-8') as json_file:
#     json.dump(all_Pets, json_file,ensure_ascii=False)

print(getPetDetailByNo(1881204334306883268))

# page1 = theMarket(headers,1)
# page2 = theMarket(headers,2)
# print(page1)
# print(page2)
