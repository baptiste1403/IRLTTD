from model.Path import Path
from model.Truck import Truck

class Trip:
    def __init__(self, path: Path, truck: Truck):
        self.__path = path
        self.__truck: Truck = truck
        self.__currentRoadPart = 0
        self.__coordinate = path.getRoadPartAt(0)
        self.__distanceFromPrevious = 0

    def getPosition(self):
        return self.__coordinate

    def getRoute(self):
        return self.__path

    def moveTruck(self, seconds: float):
        distance = float(self.__truck.getSpeed()) * seconds + self.__distanceFromPrevious
        for roadPartIndex in range(self.__currentRoadPart, self.__path.getNbPoint()):
            if roadPartIndex == self.__path.getNbPoint()-1:
                self.__currentRoadPart = self.__path.getNbPoint()
                break
            if distance > self.__path.getRoadDistanceAt(roadPartIndex):
                distance -= self.__path.getRoadDistanceAt(roadPartIndex)
            else:
                coef: float = distance / self.__path.getRoadDistanceAt(roadPartIndex)
                shift = self.__lerpCoordinates(self.__path.getRoadPartAt(roadPartIndex), self.__path.getRoadPartAt(roadPartIndex+1), coef)
                self.__coordinate = (self.__path.getRoadPartAt(roadPartIndex)[0] + shift[0], self.__path.getRoadPartAt(roadPartIndex)[1] + shift[1])
                self.__currentRoadPart = roadPartIndex
                self.__distanceFromPrevious = self.__path.getRoadDistanceAt(roadPartIndex) - distance
                break
        
        if self.__currentRoadPart == self.__path.getNbPoint():
            self.__coordinate = self.__path.getRoadPartAt(self.__path.getNbPoint()-1)
            self.__distanceFromPrevious = 0

    #(lon, lat)
    def __lerpCoordinates(self, point1, point2, coef: float):
        lat = (point2[0] - point1[0]) * coef
        lon = (point2[1] - point1[1]) * coef
        return (lat, lon)

    def getTruck(self):
        return self.__truck
