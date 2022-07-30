import json

import folium


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

def generateMap(trips):

    m = folium.Map(zoom_start=1)

    for trip in trips.values():

        folium.PolyLine(
        trip.getRoute().getPath(),
        weight=8,
        color='blue',
        opacity=0.6
        ).add_to(m)

        folium.Marker(
            location=trip.getRoute().getRoadPartAt(0),
            icon=folium.Icon(icon='play', color='green'),
        ).add_to(m)

        folium.Marker(
            location=trip.getRoute().getRoadPartAt(trip.getRoute().getNbPoint()-1),
            icon=folium.Icon(icon='stop', color='red')
        ).add_to(m)

        folium.Marker(
            location=trip.getPosition(),
            icon=folium.Icon(icon='stop', color='blue'),
            tooltip=folium.Tooltip(trip.getTruck().getName())
        ).add_to(m)

    m.save("worldmap.html")