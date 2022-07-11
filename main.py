import os 
import requests
import json
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from Keep_Alive import keep_alive

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)


#ON READY
@client.event
async def on_ready():
    topic_date.start()
    currency_activity.start()
    print("\n" + client.user.name)
    print("Main Cog is ready.")
    print(f"ping is {round(client.latency * 1000)}ms")
    print(f"bot id: {client.user.id}")
    print('-' * 25)


#ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Valamit elirtál, vagy nem létező parancsot akartál használni! ajánlom figyelmedbe a .help parancsot."
        )


#COGS LOAD
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} Cog Loaded!")


#COGS RELOAD
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} Cog Reloaded!")


#COGS UNLOAD
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} Cog Unloaded!")


#DEFAULT COG LOAD
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


# CSEVŐ DATE
def now_time():
    now = datetime.now()
    two_hours_ago = (now + timedelta(hours=2))
    return two_hours_ago.strftime("%B %d %A")


def getCurrentValue(to_, from_, amount_ = 1):
    url = f'https://api.apilayer.com/exchangerates_data/convert?to={to_}&from={from_}&amount={amount_}'
  
    payload = {}
    headers= {
      "apikey": "zDPMAwoYdEMKqJBqGL1keAst14yBFqEc"
    }
    
    response = requests.request("GET", url, headers=headers, data = payload)
    json_response = response.json()
    response_string = f'{amount_} {from_} -> {json_response["result"]:.2f} {to_}'
    
    return response_string

# Change currency
#@client.command()
#async def change(ctx, to_, from_, amount_ = 1):
#    await ctx.send(f"{getCurrentValue(to_, from_, amount_)} Cog Unloaded!")

# CSEVŐ DATE UPDATE
@tasks.loop(seconds=300)
async def topic_date():
    channel = client.get_channel(588731637747941397)  #csevő id
    await channel.edit(topic=now_time())   

# current currency Activity
@tasks.loop(seconds=14400)
async def currency_activity():
    await client.change_presence(activity=discord.Game(name=getCurrentValue('HUF', 'EUR')))



keep_alive()
client.run(os.environ['key'])
