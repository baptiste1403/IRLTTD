import copy
from model.Truck import Truck


class Company:
    def __init__(self, author, name, localisation: int):
        self.__author = author
        self.__name = name
        self.__money = 500000
        self.__localisation = localisation
        self.__trucks = []

    def getName(self):
        return self.__name

    def getMoney(self):
        return self.__money

    def getLocalisation(self):
        return self.__localisation

    def addTruck(self, truck: Truck):
        if truck in self.__trucks:
            return -1
        else:
            self.__trucks.append(truck)

    def getTrucks(self):
        return copy.copy(self.__trucks)