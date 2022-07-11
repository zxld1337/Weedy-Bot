import discord
from discord.ext import commands, tasks

from datetime import datetime, timedelta
from PIL import Image
import random
import time
import requests


class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Data_path = "/home/runner/WeedyBot2/cogs/Data/" 
        # for poke inits 
        self.channels = (891773145785180221,705382410531110992)
        self.poke_in_progress = []
    
    # ON READY
    @commands.Cog.listener()
    async def on_ready(self):
        print(" - Basic Cog Loaded.")

    # PING
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"**Pong!** Késleltetés: {round(self.client.latency * 1000)}ms")

    # CLEAR
    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)

    # LUCK 
    @commands.command()
    async def luck(self, ctx):
        with open(self.Data_path+"luck.txt", "r", encoding="utf-8") as f:
            await ctx.send(random.choice([row.strip() for row in f]))

    # COIN Flip 
    @commands.command()
    async def flip(self, ctx):
        await ctx.send(f"Érme oldala: "+random.choice(("Irás", "Fej")))

    # CALCULATOR 
    @commands.command()
    async def calc(self, ctx, num1: str, symbol: str, num2: str):
        expression = num1 + symbol + num2
        await ctx.send(f"Az eredmény: {float(eval(expression))}") 


    # COMMAND POKE 
    @commands.command(name="poke")
    async def poke(self, ctx, member: discord.Member, round=10):
        zxld = "311499790200340490"
        ctx_id = str(ctx.message.author.id)
        re_channel = ctx.message.author.voice.channel

        if round > 20 and ctx_id != zxld:
            await ctx.send("Max 20 lehet!")
        else:    
            for i in range(round):
                channel = self.client.get_channel(random.choice(self.channels))
                try:
                    if channel != re_channel:
                        await member.move_to(channel)
                    if round-1 == i:
                        await member.send("Megpoke-oltak!")  
                except:
                    print("member_move ERROR")
                time.sleep(1)
            
            await member.move_to(re_channel)

    # DEAFEN POKE 
    async def poke_v2(self, member: discord.Member, round: int, before):
        re_channel = before.channel
        
        for i in range(round):
            channel = self.client.get_channel(random.choice(self.channels))
            try:
                if channel != re_channel:
                    await member.move_to(channel)
                if round-1 == i:
                    await member.send("Megpoke-oltak!")
            except:
                print("member_move ERROR")
            time.sleep(1)

        await member.move_to(re_channel)   
        self.poke_in_progress.remove(str(member))

    # DEAFEN POKE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.deaf and str(member) not in self.poke_in_progress:
            self.poke_in_progress.append(str(member))
            await member.edit(deafen = False)
            await self.poke_v2(member, 7, before)
            

    # Image Rotate
    @commands.command()
    async def rotate(self, ctx, deg=None):
        if not deg:
            await ctx.send("Na és honnan találjam ki hány fokban kell megforditani a képet?")
            await ctx.send("Szóval mennyire kéne?")
            reply = await self.client.wait_for('message')
            deg = reply.content

            await ctx.send("És most jöhet a kép amit meg kell csűrnöm")
        else:
            await ctx.send("A képet legyen szives!")

        img = await self.client.wait_for('message')
        needtoformat = img.attachments[0]
        
        response = requests.get(needtoformat.url)
        file = open(f"{self.Data_path}nfi_image.png", "wb")
        file.write(response.content)
        file.close()

        image = Image.open(f"{self.Data_path}nfi_image.png")
        rotated = image.rotate(int(deg))
        rotated.save(f"{self.Data_path}rotated_img.png")

        await ctx.send(file=discord.File(f'{self.Data_path}rotated_img.png'))


    # Return Date GMT+02:00
    def now_time():
        now = datetime.now()
        two_hours_ago = (now + timedelta(hours=2))
        return two_hours_ago.strftime("%B %d %A")


def setup(client):
    client.add_cog(Basic(client))