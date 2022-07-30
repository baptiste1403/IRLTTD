import polyline
import util.api as api

class Path:
    def __init__(self, city1: int, city2: int):
        self._city1 = city1
        self._city2 = city2
        route = api.getRouteBetweenCity(city1, city2)
        self._route = polyline.decode(route['geometry'])
        self._distances = route['legs'][0]['annotation']['distance']
    
    def __str__(self):
        return f"between {self._city1} and {self._city2}"

    def getRoadPartAt(self, index: int):
        return self._route[index]

    def getRoadDistanceAt(self, index: int):
        return self._distances[index]

    def getNbPoint(self):
        return len(self._distances)+1

    def getPath(self):
        return self._route