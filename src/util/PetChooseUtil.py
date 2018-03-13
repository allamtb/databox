
from util.ConfigUtil import  *

def choose_pet(pets):

    # method 1 通过定义规则来选择
    valid_pets = []
    for pet in pets:
        amount = float(pet.get(u"amount"))
        petRare = str(pet.get(u"rareDegree"))
        config = getPriceConfig()
        if amount < float(config[petRare]):
            valid_pets.append(pet)
    return valid_pets
    # method 2 通过当前市场的价格分布，选择分布在-2a区间的
    # method 3 通过机器学习预测走势来分析中间价格
