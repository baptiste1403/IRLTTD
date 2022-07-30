import json


class Package:
    def __init__(self, item, qte: int):
        f = open("data/items.json")
        result = json.load(f)
        
        if result[item] == None:
            raise ValueError("cannot load the given type")

        self.__item = item
        self.__quantity = qte
        self.__singleBulk = int(result[item]['bulk'])
        self.__bulk = qte * self.__singleBulk

    def getItem(self):
        return self.__item

    def getQuantity(self):
        return self.__quantity

    def getBulk(self):
        return self.__bulk

    def setQuantity(self, qte: int):
        self.__quantity = qte
        self.__bulk = qte * self.__singleBulk