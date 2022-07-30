from aiohttp import TraceRequestChunkSentParams
import folium
from model.Path import Path
from model.Truck import Truck
from model.Trip import Trip


code1 = 45208
code2 = 45004

path = Path(code1, code2)
truck = Truck("basic-truck", "Martin")
trip = Trip(path, truck)

print(trip.getPosition())

trip.moveTruck(180)

print(trip.getPosition())

m = folium.Map(zoom_start=1)

folium.PolyLine(
    path.getPath(),
    weight=8,
    color='blue',
    opacity=0.6
).add_to(m)

folium.Marker(
    location=path.getRoadPartAt(0),
    icon=folium.Icon(icon='play', color='green')
).add_to(m)

folium.Marker(
    location=path.getRoadPartAt(path.getNbPoint()-1),
    icon=folium.Icon(icon='stop', color='red')
).add_to(m)

folium.Marker(
    location=trip.getPosition(),
    icon=folium.Icon(icon='stop', color='blue')
).add_to(m)

m.save("test.html")