class Path:
    def __init__(self, distance: float, duration: float):
        self._distance = distance
        self._duration = duration
    
    def __str__(self):
        return f"{self._distance} km ({self._duration} h)"