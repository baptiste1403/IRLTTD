import json


def getFactoriesInfo():
    f = open("data/industries.json")
    data = json.load(f)

    res = "```\n"
    for key in data.keys():
        value = data[key]
        res += f" * {key} :\n"
        if value['need'] != None:
            res += "\t- need :\n"
            for need in value['need']:
                res += f"\t\t{need['item']}, qte : {need['quantity']} tonnes/jour/1000 hab\n"

        if value['product'] != None:
            res += "\t- produce :\n"
            for product in value['product']:
                res += f"\t\t{product['item']}, qte : {product['quantity']} tonnes/jour/1000 hab\n"
        
        res += "\n"

    res += "```"
    f.close()
    return res