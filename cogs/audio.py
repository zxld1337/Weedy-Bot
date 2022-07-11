import discord
from discord.ext import commands
from discord.player import FFmpegPCMAudio

from pytube import YouTube
import os

class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.song_path = "/home/runner/WeedyBot2/cogs/"
        # soundboard
        self.indexes = []
        self.emotes = ("0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", "⚪","⚫","🔴","🔵","🟤","🟣","🟢")
   

    #ON READY
    @commands.Cog.listener()
    async def on_ready(self):
        print(" - Audio Cog Loaded.")

    # JOIN
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()   
        else:
            await ctx.send("Nem vagy csatlakozva egy hangszobához se!")

    # LEAVE
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Nem vagyok hangszobához csatlakozva!")

    # PAUSE
    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Nem tudom te mikbe vagy, de semmilyen zene nem megy most!")

    # RESUME
    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Semmilyen zene nincs megállitva!")

    # STOP
    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()


    # DOWNLOAD SONG
    def yt_dl(self, url):
        youtube = YouTube(url).streams.get_audio_only().download(self.song_path+"Soundboard/")
        return youtube

    # PLAY
    @commands.command()
    async def play(self, ctx, url):
        path = self.yt_dl(url)
        if ctx.author.voice and not ctx.voice_client:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        elif not ctx.author.voice: 
            await ctx.send("Csatlakoz egy hangcsatornába!")
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(path)
        voice.play(source)

    # COLLECTING ALL SOUNDS
    def collect_sounds(self):
        path = self.song_path+"Soundboard/"
        global soundboard_list
        soundboard_list = [name.rstrip(".mp3").strip() for name in os.listdir(path)]


    # SoundBoard
    @commands.command()
    async def soundboard(self, ctx):
        print("start")
        self.collect_sounds()
        if ctx.author.voice and not ctx.voice_client:
            print("in if")
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            print("after conn")
        elif not ctx.author.voice: 
            await ctx.send("Csatlakoz egy hangcsatornába!")
            return
        icon = "https://content.instructables.com/ORIG/FP4/S4E0/GRFMW48T/FP4S4E0GRFMW48T.jpg?auto=webp"
        embed=discord.Embed(title="Soundboard", color=0x0635e0)
        
        for i, item in enumerate(soundboard_list):
            embed.add_field(name=f"{self.emotes[i]} - {item}", value=f"|", inline=True)
        embed.set_thumbnail(url=icon)
        message = await ctx.send(embed=embed)

        for emote in self.emotes:
            await message.add_reaction(emote) 
        global voice_in_room 
        voice_in_room = discord.utils.get(self.client.voice_clients, guild=ctx.guild)        


    # Youtube-Downloader
    @commands.command()
    async def ytd(self, ctx, url: str, vtype="audio"):
        path = YouTube(url).streams.filter(type=vtype).first().download(self.song_path+"Song/")
        try:
            await ctx.send(file=discord.File(path))
            await ctx.send(f"**{ctx.message.author.name}** itt a letöltött file-od.")
        except:
            await ctx.send("Valami hiba történt! Lehet hogy túl nagy a file!")

        os.remove(path)


    # Soundboard Reaction Event
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        if user.id != self.client.user.id:
            if reaction.emoji in self.emotes:
                ind = self.emotes.index(reaction.emoji)
                source = FFmpegPCMAudio(f"{self.song_path}/Soundboard/{soundboard_list[ind]}.mp3")
                try:
                    voice_in_room.play(source)
                except:
                    pass

def setup(client):
    client.add_cog(Audio(client))