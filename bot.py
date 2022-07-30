from ctypes import util
import os
from unicodedata import name
from model.Company import Company
from model.Path import Path
from model.Trip import Trip
from model.Truck import Truck

import util.plot as plot
from model.City import City
import util.api as api
import util.utils as utils
import networkx as nx

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

graph = nx.Graph()

trips = {}
paths = {}
companies = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@tasks.loop(seconds=10)
async def updater():
    global trips
    for trip in trips.values():
        trip.moveTruck(10)
    utils.generateMap(trips)

@bot.event
async def on_ready():
    print("I'm now connected !!!")
    updater.start()

@bot.command(name='searchcity', help="search city info by name")
async def search_city(ctx, name):
    cities = api.cities(name)
    res = ""
    for city in cities:
        res += f"{city['name']}, {city['dep']}, {city['reg']}, INSEE({city['code']})\n"
    print(res)
    await ctx.send(res)

@bot.command(name='addcity', help='add city to the card with the INSEE code')
async def add_city(ctx, code: int):
    dictCity = api.cityByINSEE(code)
    if dictCity == None:
        await ctx.send("invalid INSEE code")
    
    global graph
    cur = City(dictCity['name'], int(dictCity['pop']), float(dictCity['surface']), code)
    graph.add_node(int(code), city=cur)
    for id, city in graph.nodes(data='city'):
        if city != cur:
            graph.add_edge(city.getCode(), cur.getCode(), path=api.distanceBetweenCity(city.getCode(), cur.getCode()))

    plot.createImageFromGraph(graph)
    with open("fig.png", "rb") as fh:
        f = discord.File(fh, filename="fig.png")
    await ctx.send(f"{dictCity['name']}, pop : {dictCity['pop']} inhabitants, surface : {dictCity['surface']} m²", file=f)

@bot.command(name='cityindustry', help='give informations about the industry of this city')
async def city_industry(ctx, code: int):
    dictCity = api.cityByINSEE(code)
    if dictCity == None:
        await ctx.send("invalid INSEE code")

    cur = City(dictCity['name'], int(dictCity['pop']), float(dictCity['surface']), code)
    await ctx.send(cur.getIndustries())

#@bot.command(name='showmap', help='show the map as a graph')
#async def city_industry(ctx):
#    plot.createImageFromGraph(graph)
#    with open("fig.png", "rb") as fh:
#        f = discord.File(fh, filename="fig.png")
#    await ctx.send(file=f)

@bot.command(name='industriesinfo', help="list all industry types")
async def industries_info(ctx):
    await ctx.send(utils.getFactoriesInfo())

@bot.command(name="depsuppliers", help="give a list of suppliers in dep")
async def dep_supplier(ctx, code: int):
    await ctx.send(api.getDepartmentSupliers(code))

@bot.command(name="depclients", help="give a list of clients in dep")
async def dep_supplier(ctx, code: int):
    await ctx.send(api.getDepartmentClient(code))

 #create a new company 
@bot.command(name="createcompany", help="create a new company")
async def create_company(ctx, name: str):
    global companies
    print(ctx.author.id)
    if ctx.author.id not in companies.keys():
        companies[ctx.author.id] = Company(ctx.author.name, name, 75056)
        await ctx.send(f"company {name} created")
    else:
        await ctx.send("you already have a company")

@bot.command(name="addtrip", help="add a trip for one of your truck")
async def add_trip(ctx, name, code1: int, code2: int):
    if api.cityByINSEE(code1) == None or api.cityByINSEE(code2) == None:
        await ctx.send("code incorrect")
        return

    global companies
    if ctx.author.id not in companies.keys():
        await ctx.send("you don't own a company")
        return
        
    global paths
    if (code1, code2) not in  paths.keys():
        paths[(code1, code2)] = Path(code1, code2)
    
    global trips
    truck = Truck("basic-truck", name)
    trips[f"{companies[ctx.author.id].getName()}_{name}"] = Trip(paths[(code1, code2)], truck)
    
    await ctx.send(f"trip for the truck {name} added")

@bot.command(name="miao", help="miao")
async def miao(ctx):
    await ctx.send("miao")

bot.run(TOKEN)