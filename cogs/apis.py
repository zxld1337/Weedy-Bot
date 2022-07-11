import discord
from discord.ext import commands


import requests


class Api(commands.Cog):
    def __init__(self, client):
        self.client = client

    #ON READY
    @commands.Cog.listener()
    async def on_ready(self):
        print(" - Api Cog Loaded.")

    # LOL STATS API
    @commands.command()
    async def lolstat(self, ctx, name):
        apikey = 'api KEY HERE'
        url = f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={apikey}'
        res = requests.get(url)
        data = res.json()
        
        id = data["id"]
        proficonID = data["profileIconId"]

        profile_icon = f"https://ddragon.leagueoflegends.com/cdn/11.13.1/img/profileicon/{proficonID}.png"
        #playermain_url = f"http://ddragon.leagueoflegends.com/cdn/11.13.1/img/champion/{main}.png"

        summonerurl = f"https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={apikey}"
        res = requests.get(summonerurl)
        DATA = res.json()

        TYPE_1 = DATA[1]["queueType"]

        FLEX_TIER = DATA[1]["tier"]
        FLEX_RANK = DATA[1]["rank"]
        FLEX_LP = DATA[1]["leaguePoints"] 
        FLEX_WIN = DATA[1]["wins"]
        FLEX_LOSE = DATA[1]["losses"]

        SD_TIER = DATA[0]["tier"]
        SD_RANK = DATA[0]["rank"]
        SD_LP = DATA[0]["leaguePoints"] 
        SD_WIN = DATA[0]["wins"]
        SD_LOSE = DATA[0]["losses"]

        if TYPE_1 == "RANKED_SOLO_5x5":
            RANK = FLEX_TIER.lower()
            MODE0 = "SOLO/DUO"
            MODE1 = "FLEX"
        else:
            RANK = SD_TIER.lower()
            MODE0 = "FLEX"
            MODE1 = "SOLO/DUO"

        embed = discord.Embed(title=f"{name}", colour=discord.Colour(0xda9547), url=f"https://eune.op.gg/summoner/userName={name}")

        #rank_pic = f"https://www.theloadout.com/wp-content/uploads/2019/09/league-of-legends-{RANK}-rank.jpg"
        rank_pic = f"https://opgg-static.akamaized.net/images/medals/{RANK}_1.png?image=q_auto:best&v=1"

        embed.set_image(url=rank_pic)
        embed.set_thumbnail(url=profile_icon)

        embed.add_field(name=MODE0, value=f"- RANK: {FLEX_TIER} {FLEX_RANK}\n- LP: {FLEX_LP}\n- WINS: {FLEX_WIN}\n- LOSES: {FLEX_LOSE}", inline=False)
        embed.add_field(name=MODE1, value=f"- RANK: {SD_TIER} {SD_RANK}\n- LP: {SD_LP}\n- WINS: {SD_WIN}\n- LOSES: {SD_LOSE}", inline=False)

        await ctx.send(embed=embed)


    #WEATHER API 
    @commands.command()
    async def weather(self, ctx, city: str):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=APIKEYHERE='
        res = requests.get(url)
        data = res.json()

        name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp'] - 273.15
        temp_feels = data['main']['feels_like'] - 273.15
        wind_speed = data['wind']['speed'] * 3.6
        visibility = data['visibility'] / 1000
        description = data['weather'][0]['description']
        
        temp_emb = discord.Embed(title="Időjárás", description=f"{name}, {country}", color=0x0ea8b0)
        temp_emb.set_thumbnail(url="https://blog.atomicsmash.co.uk/wp-content/uploads/2019/02/WeatherPress-Plugin.png")
        temp_emb.add_field(name='Hőmérséklet', value=f"{round(temp, 1)} C", inline=False)
        temp_emb.add_field(name='Hőérzet', value=f"{round(temp_feels, 1)} C", inline=False)
        temp_emb.add_field(name='Szél', value=f"{round(wind_speed, 1)} km/h", inline=False)
        temp_emb.add_field(name='Leirás', value=f"{description}", inline=False)
        
        await ctx.send(embed=temp_emb)


def setup(client):
    client.add_cog(Api(client))
