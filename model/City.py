import json
import numpy as np

class City:
    def __init__(self, name, inhabitants: int, surface: float, code: int):
        self._name = name
        self._inhabitants = inhabitants
        self._surface = surface
        self._code = code
    
    def __str__(self):
        return f"{self._name}({self._inhabitants})"

    def getCode(self):
        return self._code

    def getIndustriesKey(self):
        f = open("data/industries.json")
        data = json.load(f)
        np.random.seed(self._code)
        return list(data.keys())[np.random.randint(0, len(data))]

    def getIndustries(self):
        f = open("data/industries.json")
        data = json.load(f)
        np.random.seed(self._code)
        key = list(data.keys())[np.random.randint(0, len(data))]
        factory = data[key]

        res = f"factory in {self._name} is a {key}\n"
        if factory['need'] != None:
            res += "- need :\n"
            for need in factory['need']:
                res += f"\t{need['item']}, qte : {round(need['quantity'] * (self._inhabitants/1000.0), 3)} tonnes/jour\n"

        if factory['product'] != None:
            res += "- produce :\n"
            for product in factory['product']:
                res += f"\t{product['item']}, qte : {round(product['quantity'] * (self._inhabitants/1000.0), 3)} tonnes/jour\n"

        f.close()
        return res