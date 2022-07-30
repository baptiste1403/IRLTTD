import copy
from model.Package import Package
import json


class Truck:
    def __init__(self, type, name):
        f = open("data/trucks.json")
        result = json.load(f)
        
        if result[type] == None:
            raise ValueError("cannot load the given type")
        
        self.__type = result[type]
        self.__capacity = int(result[type]['capacity'])
        self.__speed = int(result[type]['speed'])
        self.__content = {}
        self.__name = name

        f.close()

    def getType(self):
        return self.__type

    def getCapacity(self):
        return self.__capacity

    def getSpeed(self):
        return self.__speed

    def getName(self):
        return self.__name

    def getContentBulk(self):
        res = 0
        for pack in self.__content.values():
            res += pack.getBulk()
        return res

    def addContent(self, pack: Package):
        if pack.getBulk() + self.getContentBulk() > self.__capacity:
            return -1
        
        if pack.getItem() in self.__content.keys():
            actualpack = self.__content[pack.getItem()]
            actualpack.setQuantity(actualpack.getQuantity() + pack.getQuantity())
        else:
            self.__content[pack.getItem()] = pack

    def getContent(self):
        return copy.deepcopy(self.__content)

    def __eq__(self, other) -> bool:
        if isinstance(other, Truck):
            return self.__name == other.getName()
        return False