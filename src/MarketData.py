from __future__ import unicode_literals

import queue
from util.RequestUtil import *
from util.PetChooseUtil import choose_pet
from util.ConfigUtil import *
# 打印堆栈信息
import traceback

def getPetsMultiThread(mission_queue, result_queue):
    while mission_queue.qsize() > 0:
        page_no = mission_queue.get()
        page_no += 1
        print("线程号{},处理页数{}".format(threading.currentThread().name, page_no))
        try:
            pets = getMarketData(page_no).get(u"data").get("petsOnSale")
            print("第{}页获取到的pets{}".format(page_no, pets))
            if pets:
                result_queue.put(pets)
                # get_detail(pets)
        except Exception as e:
            traceback.print_exc()
            print("由于链接百度失败 {}，组织决定补采该页数据页 {}".format(e, page_no))
            mission_queue.put(page_no)


def get_detail(pets):
    for pet in pets:
        petId = str(pet.get(u"petId"))
        petDetail = getPetDetailByPetId(petId)
        print("莱特狗信息{}，详细信息{}".format(pet, petDetail))


def getCurrentAllMarketPet(result_queue):
    totalPageSize = getTotalPages()
    mission_queue = queue.Queue()
    [mission_queue.put(i) for i in range(int(totalPageSize))]

    # 创建多线程
    threadPool = []
    threadNum = int(getSysConfig()['marketthread'])
    for i in range(threadNum):
        t = threading.Thread(target=getPetsMultiThread, args=(mission_queue, result_queue))
        t.start()
        threadPool.append(t)
    # join加入到主线程中,使主线程阻塞
    for t in threadPool:
        t.join()


def getAllValidMarketPet():
    time1 = time.time()
    resultQueue = queue.Queue()
    getCurrentAllMarketPet(resultQueue)
    print("市场数据获取完毕")
    allPets = []
    qsize = resultQueue.qsize()
    while resultQueue.qsize() > 0:
        pets = resultQueue.get()
        validPets = choose_pet(pets)
        if validPets:
            allPets.append(validPets)
    time2 = time.time()
    print("花费了{}秒,获取到{}页,经过删选后还剩{},pets详情如下{}".format(time2 - time1, qsize, allPets, len(allPets)))
    return allPets



if __name__ == '__main__':

    getAllValidMarketPet()