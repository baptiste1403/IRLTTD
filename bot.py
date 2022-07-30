import os
from unicodedata import name

import plot
from City import City
import api
import utils
import networkx as nx

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

graph = nx.Graph()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@tasks.loop(seconds=1)
async def updater():
    pass

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

@bot.command(name='showmap', help='show the map as a graph')
async def city_industry(ctx):
    plot.createImageFromGraph(graph)
    with open("fig.png", "rb") as fh:
        f = discord.File(fh, filename="fig.png")
    await ctx.send(file=f)

@bot.command(name='industriesinfo', help="list all industry types")
async def industries_info(ctx):
    await ctx.send(utils.getFactoriesInfo())

@bot.command(name="depsuppliers", help="give a list of suppliers in dep")
async def dep_supplier(ctx, code: int):
    await ctx.send(api.getDepartmentSupliers(code))

@bot.command(name="depclients", help="give a list of clients in dep")
async def dep_supplier(ctx, code: int):
    await ctx.send(api.getDepartmentClient(code))

bot.run(TOKEN)