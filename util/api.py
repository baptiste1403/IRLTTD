import json
import time
import requests as req
from model.City import City

from model.Path import Path

def cities(name):
    res = []

    result = req.get(f'https://geo.api.gouv.fr/communes?nom={name}&fields=code,nom,departement,region')

    for city in result.json():
        res.append({'name': city['nom'], 'dep': city['departement']['nom'], 'reg': city['region']['nom'], 'code': city['code']})

    return res

def cityByINSEE(code: int):
    res = {}

    result = req.get(f'https://geo.api.gouv.fr/communes/{code}?fields=nom,surface,population,departement')

    if result.status_code != 200:
        return None

    dictResult = result.json()

    res['name'] = dictResult['nom']
    res['surface'] = dictResult['surface']
    res['pop'] = dictResult['population']
    res['dep'] = dictResult['departement']['code']

    return res

def distanceBetweenCity(code1: int, code2: int) -> Path:

    r1 = req.get(f'https://geo.api.gouv.fr/communes/{code1}?fields=code,nom,centre')
    lat1 = r1.json()['centre']['coordinates'][0]
    lon1 = r1.json()['centre']['coordinates'][1]

    r2 = req.get(f'https://geo.api.gouv.fr/communes/{code2}?fields=code,nom,centre')
    lat2 = r2.json()['centre']['coordinates'][0]
    lon2 = r2.json()['centre']['coordinates'][1]

    result = req.get(f'http://router.project-osrm.org/route/v1/driving/{lat1},{lon1};{lat2},{lon2}?overview=false')

    route = result.json()['routes'][0]
    return Path(round(float(route['distance'])/1000.0, 2), round(float(route['duration'])/3600.0, 2))


def getDepartmentSupliers(code: int):
    city = cityByINSEE(code)
    if city == None:
        return None

    f = open("data/industries.json")

    datas = json.load(f)

    dep = city['dep']
    result = req.get(f"https://geo.api.gouv.fr/departements/{dep}/communes?fields=nom,surface,population")

    listResult = result.json()

    ori = City(city['name'], city['pop'], city['surface'], code)
    print(ori.getIndustriesKey())
    if(datas[ori.getIndustriesKey()]['need'] == None):
        return []

    oriIndustryNeed = list(map(lambda x : x['item'], datas[ori.getIndustriesKey()]['need']))

    res = []

    for value in listResult:
        cur = City(value['nom'], int(value['population']), float(value['surface']), int(value['code']))
        curIndustryKey = cur.getIndustriesKey()

        if(datas[curIndustryKey]['product'] == None):
            continue

        curIndustryProduct = list(map(lambda x : x['item'], datas[curIndustryKey]['product']))

        
        if any(check in curIndustryProduct for check in oriIndustryNeed):
            res.append(value['code'])
            print(f"cur : {curIndustryProduct}")

    print(res)
    return res

def getDepartmentClient(code: int):
    city = cityByINSEE(code)
    if city == None:
        return None

    f = open("data/industries.json")

    datas = json.load(f)

    dep = city['dep']
    result = req.get(f"https://geo.api.gouv.fr/departements/{dep}/communes?fields=nom,surface,population")

    listResult = result.json()

    print(listResult)

    ori = City(city['name'], city['pop'], city['surface'], code)
    if(datas[ori.getIndustriesKey()]['product'] == None):
        return []

    oriIndustryProduct = list(map(lambda x : x['item'], datas[ori.getIndustriesKey()]['product']))

    res = []

    for value in listResult:
        cur = City(value['nom'], int(value['population']), float(value['surface']), int(value['code']))
        curIndustryKey = cur.getIndustriesKey()

        if(datas[curIndustryKey]['need'] == None):
            continue

        curIndustryNeed = list(map(lambda x : x['item'], datas[curIndustryKey]['need']))

        
        if any(check in curIndustryNeed for check in oriIndustryProduct):
            res.append(value['code'])
            print(f"cur : {curIndustryNeed}")

    return res