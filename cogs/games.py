from discord.ext import commands
import discord

from datetime import datetime, timedelta
import random



class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.emotes = ("✅", "❌", "🔄", "🔊")
        self.channels = ("694936944072720394", "705074550324461749", "705382410531110992", "705447281251320371", "743164769229340683", "703742940685795409")

        self.message = None
        self.pubg_members = []
        self.channels_with_names = []
        self.teams_vchannels = {}


    #ON READY
    @commands.Cog.listener()
    async def on_ready(self):
        print(" - Games Cog Loaded.")


    # GET CURRENT TIME
    def now_time(self):
        now = datetime.now()
        two_hours_ago = (now + timedelta(hours=2))
        return two_hours_ago.strftime("%B %d %A")    
    
    
    # GET CHANNEL NAMES
    def get_names(self, xtc):
        for channel in xtc.guild.voice_channels:
            if str(channel.id) in self.channels:
                self.channels_with_names.append([channel.name, channel.id])  
                

    # LOBBY MAKER
    @commands.command()
    async def lobby(self, ctx):
        self.get_names(ctx)

        # start embed
        embed = discord.Embed(title="Lobby Maker", colour=discord.Colour(0x45f542))
        #embed.set_thumbnail(url="https://thestartupgen.com/wp-content/uploads/2019/10/team.jpg")

        # get players if pubg role
        members_len = len(ctx.guild.get_role(889875786889302027).members)
        self.pubg_members = [(x.name, x.id) for x in ctx.guild.get_role(889875786889302027).members]
        if members_len % 2 != 0: self.pubg_members.append(("x", "021034054315"))
        random.shuffle(self.pubg_members)

        # display players on embed
        tnum = 1
        for i in range(0, len(self.pubg_members), 2): #889875786889302027 #889877101694566441
            embed.add_field(name=f"Team {tnum}", value=f"```{self.pubg_members[i][0]} - {self.pubg_members[i+1][0]}``` - {self.channels_with_names[tnum][0]}", inline=False)

            # get player names and ids
            self.teams_vchannels[self.channels_with_names[tnum][1]] = [self.pubg_members[i][1], self.pubg_members[i+1][1]]            
            tnum += 1

        embed.add_field(name="✅ - Megkapod a pubg role-t, és benne leszel a sorsolásban.", value="** **", inline=False)
        embed.add_field(name="❌ - Leszedi a pubg role-t, nem leszel benne a sorsolásban. ", value="** **", inline=False)
        embed.add_field(name="🔄 - In progress", value="** **", inline=False)
        embed.add_field(name="🔊 - Elvisz a team alatti szobába. Ha kezdődik a meccs akkor használd.", value="** **", inline=False)

        self.message = await ctx.send(embed=embed)

        # add reacts
        for emote in self.emotes:
            await self.message.add_reaction(emote)


            
    # LOBBY REACTION EVENT 
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        if user.id != self.client.user.id:
            role = discord.utils.get(user.guild.roles, name="pubg")
            if reaction.emoji == "✅":
                await user.add_roles(role)
            elif reaction.emoji == "❌":
                await user.remove_roles(role)
            elif reaction.emoji == "🔄":
                print("nem működik")
            elif reaction.emoji == "🔊":
                for key, value in self.teams_vchannels.items():
                    for ember in value:
                        if user.id == ember:
                            channel = self.client.get_channel(key)
                            try:
                                await user.move_to(channel)
                            except:
                                pass
                        

    # Lobby cleaner
    @commands.command()
    async def clearlobby(self, ctx):
        for user in ctx.guild.fetch_members(limit=None):
            role = discord.utils.get(user.guild.roles, name="pubg")
            user.remove_roles(role)
                






def setup(client):
    client.add_cog(Games(client))


    
    