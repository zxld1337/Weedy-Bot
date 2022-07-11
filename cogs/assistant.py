import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

from datetime import date, datetime, timedelta
import time 
import calendar
import pyjokes
from gtts import gTTS

class Assistant(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.assistant_path = "/home/runner/WeedyBot2/cogs/Assistant/"


    # ON READY
    @commands.Cog.listener()
    async def on_ready(self):
        print(" - Assistant Cog Loaded.")

    # RETURN THE DAY
    def tellDay(self):
        day = date.today()
        return f"The day is {calendar.day_name[day.weekday()]}"

    # RETURN THE TIME
    def tellTime(self):
        now = datetime.now()
        two_hours_ago = (now + timedelta(hours=2))
        current_time = two_hours_ago.strftime("%I:%M %p")
        return f"Your current local time is {current_time}"

    """
    # VOICE MAKER - pyttsx3
    def make_voice(self, msg: str, voice):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-90)
        engine.save_to_file(msg, self.assistant_path+"tts_msg.mp3")
        engine.runAndWait()
        source = FFmpegPCMAudio(self.assistant_path+"tts_msg.mp3")
        voice.play(source)
    """

    #VOICE MAKER - gTTS
    def make_voice(self, msg: str, voice):
        gTTS(msg, lang='en', tld='com').save(self.assistant_path+"tts_msg.mp3")
        source = FFmpegPCMAudio(self.assistant_path+"tts_msg.mp3")
        voice.play(source)


    # Weedy Text Assistant START
    @commands.command()
    async def assistant(self, ctx):
        if ctx.author.voice and not ctx.voice_client:
            channel = ctx.author.voice.channel
            voice = await channel.connect()

        voice = ctx.guild.voice_client
        msg = "Hello my name is weedy, how can I help you?"
        self.make_voice(msg, voice)


    # Text assistant ASK
    @commands.command()
    async def ask(self, ctx, *args):
        if ctx.author.voice and not ctx.voice_client:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
                
        voice = ctx.guild.voice_client 
        if "time" in args:
            msg = self.tellTime()
            self.make_voice(msg, voice)
        elif "day" in args:
            self.make_voice(self.tellDay(), voice)
        elif "joke" in args:
            self.make_voice(pyjokes.get_joke(), voice)
        elif "help" in args:
            msg = "You can ask the day, the time, ask for a joke or you can use weedy to say your text"
            self.make_voice(msg, voice)
            await ctx.send("pélada: .ask 'what day is today?' elérhető kérdések: time, day, joke, help, goodbye")
        elif "goodbye" in args:
            self.make_voice("Goodbye master", voice)
            time.sleep(2)
            await ctx.voice_client.disconnect()
            return
        else:
            msg = " ".join(args)
            self.make_voice(msg, voice)
        


def setup(client):
    client.add_cog(Assistant(client))