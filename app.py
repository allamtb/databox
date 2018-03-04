from __future__ import unicode_literals

import queue
import threading
from webutil import *
from timeit import timeit


def getPetsMultiThread(q):
    while q.qsize() > 0:
        page_no = q.get()
        page_no += 1
        print("线程号{},处理页数{}".format(threading.currentThread().name, page_no))
        try:
            pets = getMarketData(page_no).get(u"data").get("petsOnSale")
            print(pets)
            for pet in pets:
                petId = str(pet.get(u"petId"))
              #  petDetail = getPetDetailByPetId(petId)
             #   print("莱特狗信息{}，详细信息{}".format(pet, petDetail))
        except Exception as e:
            print("由于链接百度失败 {}，组织决定补采该页数据页 {}".format(str(e),page_no))
            time.sleep(0.05)
            q.put(page_no)


def getCurrentAllMarketPet():

    totalPageSize = getTotalPages()
   # all_Pets = []
    q = queue.Queue()
    [q.put(i) for i in range(int(totalPageSize))]

    # 创建多线程
    threadPool = []
    for i in range(60):
        t = threading.Thread(target=getPetsMultiThread, args=(q,))
        t.start()
        threadPool.append(t)
    #join加入到主线程中,使主线程阻塞
    for t in threadPool:
        t.join()

# time1 = time.time()
# getCurrentAllMarketPet()
#
# time2 = time.time()
# print("花费了{}秒".format(time2 - time1))

#print(getPetsByPage(140))
# for i in tqdm(range(1)):
#   #  print("当前处理到第{}页".format((i+1)))
#     all_Pets.append(getPetsByPage(i + 1))
#
# with open("all_pets.json", 'w', encoding='utf-8') as json_file:
#     json.dump(all_Pets, json_file,ensure_ascii=False)

#print(getPetDetailByPetId(1882327966471304705))
