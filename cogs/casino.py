import discord
from discord.ext import commands

import json
import random
import time

class Casino(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data_path = "/home/runner/WeedyBot2/cogs/Data/"
        self.AC_DATA = json.load(open(self.data_path+"AC_DATA.json"))
        # for roulette
        self.enters = {}
        self.enters_name = {}
        self.opt_ods = []

    #ON READY
    @commands.Cog.listener()
    async def on_ready(self):
        print(" - Casino Cog Loaded.")

    # DATA SAVE
    def AC_DATA_SAVE(self):
        save = json.dumps(self.AC_DATA, indent=2)
        with open(self.data_path+"/AC_DATA.json", "w") as file:
            file.write(save)
            file.close()

    # YOUR DATA TEST
    @commands.command()
    async def mydata(self, ctx):
        id = str(ctx.message.author.id)
        await ctx.send(self.AC_DATA[id])
    
    # USER STATS
    @commands.command()
    async def stats(self, ctx, member: discord.Member):
        User = str(member.id)
        gb = self.AC_DATA[User]['balance']
        embed = discord.Embed()
        embed.set_author(name=f"{member.name} - STATS", icon_url=member.avatar_url)
        embed.set_image(url=member.avatar_url)
        embed.add_field(name="Gempa Balance", value=f"{gb:,} G", inline=False)
        embed.set_footer(text=f"ID: {member.id}")
        await ctx.send(embed=embed)

    # GEMPA HELP TODO NEED TO REWORK
    @commands.command()
    async def ghelp(ctx):
        await ctx.send("soon available, until then use .help")

    #GEMPA BALANCE TODO rework to embed
    @commands.command()
    async def gb(self, ctx):
        id = str(ctx.message.author.id)
        Name = str(ctx.message.author.name)
        if id not in self.AC_DATA:
            self.AC_DATA[id] = {
                "name": Name,
                "id": int(id),
                "balance": 10000,
                "daily_claim": False
            }
            self.AC_DATA_SAVE()

        await ctx.send(f"<@{id}> || Egyenleged: **{self.AC_DATA[id]['balance']:,} Gempa**")


    # COIN ADD
    @commands.command()
    async def add(self, ctx, to_member: discord.Member, amount):
        if ctx.message.author.id == 311499790200340490:
            self.AC_DATA[str(to_member.id)]['balance'] += int(amount)
            self.AC_DATA_SAVE()
            await ctx.send(f"Sikeresen addoltál, {to_member.name}-nek.")
        else:
            await ctx.send("Szép álmok Lacikám!")

    # COIN TRANSFER
    @commands.command()
    async def gtransfer(self, ctx, to_member: discord.Member, amount):
        from_id = str(ctx.message.author.id)
        from_name = str(ctx.message.author.name)

        to_name = str(to_member.name)
        to_id = str(to_member.id)

        if from_id not in self.AC_DATA:
            await ctx.send(f"**{from_name}** Nincs Gempa fiokod! .gb vel birsz létrehozni.")
        elif to_id not in self.AC_DATA:
            await ctx.send(f"**{from_name}** Nem jó az id/név! Vagy nincs fiokja annak akinek utalni szeretnél!")
        elif int(amount) > self.AC_DATA[from_id]['balance']:
            await ctx.send(f"**{from_name}** Nincs ennyi az egyenlegeden!")
        elif amount[0] in ("-", "*", "/", "+"):
            await ctx.send(f"**{from_name}** annyáddal vicceskedj!")
        else:
            self.AC_DATA[from_id]['balance'] -= int(amount)
            self.AC_DATA[to_id]['balance'] += int(amount)
            
            self.AC_DATA_SAVE()
            await ctx.send(f"**{from_name}** Sikeresen utaltál **{to_name}**-nek! Utalási összeg: **{amount}** Gempa")

    

    # GempaSlot v2 TODO MAYBE DO A WRAPPER
    @commands.command()
    async def gs(self, ctx, bet="nobet"):
        symb = (":cherries:", ":watermelon:", ":grapes:")
        id = str(ctx.message.author.id)
        
        try:
            int(bet[0])
        except:
            await ctx.send(f"<@{id}> annyáddal vicceskedj!")
            return

        if bet == "allin": user_bet = self.AC_DATA[id]['balance']
        elif bet == "nobet": 
            await ctx.send("Hiányzik a bet!") 
            return
        else: user_bet = int(bet)
        
        if id not in self.AC_DATA:
            await ctx.send(f"<@{id}> Nincs Gempa fiokod! .gb vel birsz létrehozni.")
        elif user_bet > self.AC_DATA[id]['balance']:
            await ctx.send(f"<@{id}> Nincs ennyi az egyenlegeden!")
        else:
            self.AC_DATA[id]['balance'] -= user_bet
            self.AC_DATA_SAVE() 
            
            table = [random.choice(symb) for x in range(9)]
            
            embed=discord.Embed(title="Gempa Slot",  color=0x5c32a8)
            embed.set_thumbnail(url="http://adrianmarcel.com/wp-content/uploads/2020/07/screen-8-1-scaled.jpg")
            embed.add_field(name="Pörgető:", value=f"<@{id}>", inline=False)
            
            # table print into embed
            for i in range(0, 9, 3):
                embed.add_field(name="  |  ".join([table[i], table[i+1], table[i+2]]), value=" ".join("-"*11), inline=False)           
            
            # table check
            winner = 0
            all_win_amount = 0
            result = []

            for symbol in symb:
                num = table.count(symbol)
                if num > 5:
                    win = user_bet * num
                    self.AC_DATA[id]['balance'] += win
                    all_win_amount += win
                    winner += 1
                    result.append(f"{num} darab van {symbol} emoji-ból, igy {win} Gempa nyereség!")
                    
            row_num = 0
            for i in range(0, len(table), 3):
                row_num += 1
                if table[i] == table[i+1] == table[i+2]:
                    win = user_bet * 3
                    self.AC_DATA[id]['balance'] += win
                    all_win_amount += win
                    winner += 1
                    result.append(f"{table[i]} - row {row_num} - {win} Gempa nyereség!")
                    
            for i in range(3):
                if table[i] == table[i+3] == table[i+6]:
                    win = user_bet * 3
                    self.AC_DATA[id]['balance'] += win
                    all_win_amount += win
                    winner += 1
                    result.append(f"{table[i]} - column {i+1} - {win} Gempa nyereség!")
                    
            if table[0] == table[4] == table[8]:
                win = user_bet * 3
                self.AC_DATA[id]['balance'] += win
                all_win_amount += win
                winner += 1
                result.append(f"{table[0]} - cross-LR - {win} Gempa nyereség!")
                
            if table[2] == table[4] == table[6]:
                win = user_bet * 3
                self.AC_DATA[id]['balance'] += win
                all_win_amount += win
                winner += 1
                result.append(f"{table[2]} - cross-RL - {win} Gempa nyereség!")
                    
            
            if not winner:
                result.append(f"Nem nyertél! {user_bet} Gempát vesztettél!")
                embed.add_field(name="\nElemzés", value="\n".join(result), inline=False)
                lose_amount = int(bet)
                embed.add_field(name="Elvesztett összeg:", value=f"- {lose_amount:,}", inline=False)
            else:
                embed.add_field(name="\nElemzés", value="\n".join(result), inline=False)
                embed.add_field(name="Össznyeremény:", value=f"+ {all_win_amount:,}", inline=False)
                
            
            # save and embed send
            self.AC_DATA_SAVE()
            await ctx.send(embed=embed)
            


    #ROULETTE ODS
    def roulette_ods(self):
        roulette_opt = {            
                        "⬛":"⬛", 
                        "🟥":"\U0001f7e5", 
                        "🟩":"\U0001f7e9" 
        }

        oddslist = list(roulette_opt.keys())
        
        self.opt_ods.append(oddslist[2])
        for _ in range(2):
            self.opt_ods.append(oddslist[0])
            self.opt_ods.append(oddslist[1])  

    
    # ROULETTE 
    @commands.command()
    async def glette(self, ctx, bet="nobet"):
        self.roulette_ods()
        id = str(ctx.message.author.id)
        user_name = str(ctx.message.author.name)
        channel = ctx.message.channel
        
        if bet == "allin": user_bet = self.AC_DATA[id]['balance']
        elif bet == "nobet":
            await ctx.send("Hiányzik a bet!") 
            return
        else: user_bet = int(bet)
        
        try:
            int(bet[0])
        except:
            await ctx.send(f"<@{id}> annyáddal vicceskedj!")
            return
        
        if id not in self.AC_DATA:
            await ctx.send(f"<@{id}> Nincs Gempa fiokod! .gb vel birsz létrehozni.")
        elif user_bet > self.AC_DATA[id]['balance']:
            await ctx.send(f"<@{id}> Nincs ennyi az egyenlegeden!")
        else:
            self.enters.clear()
            self.enters_name.clear()
            result = random.choice(self.opt_ods)
            
            timer = 10
            for i in range(11):
                msg = f"🍀 Mindjárt pörög a kerék! 🍀"
                emb = discord.Embed(title="Roulette", description=msg, color=0xff0000)
                emb.add_field(name="Tét:", value=f"{user_bet:,}", inline=False)
                emb.set_thumbnail(url="https://media4.giphy.com/media/26uf2YTgF5upXUTm0/giphy.gif")
                if i == 0:
                    message = await ctx.send(embed=emb)
                    await message.add_reaction("⬛")  # black
                    await message.add_reaction("🟥")  # red
                    await message.add_reaction("🟩")  # green
                if timer - i == 0:
                    emb.add_field(name="Idő:", value="Most indul!", inline=False)
                    await message.edit(embed=emb)
                else:
                    emb.add_field(name="Idő:", value=f"{timer - i} Másodperc múlva indul!", inline=False)
                    await message.edit(embed=emb)
                    time.sleep(1)

            enters_id = list(self.enters)
            
            if len(enters_id) == 0: 
                await ctx.send(f"Anyádé hivod ha nem raksz gomboc **{user_name}**")
                
            tempint = False
            winners = False
    
            for i in range(len(enters_id)):
                if enters_id[i] in self.AC_DATA:
                    if self.AC_DATA[enters_id[i]]['balance'] >= user_bet:
                        self.AC_DATA[enters_id[i]]['balance'] -= user_bet
                        self.AC_DATA_SAVE()
                        if self.enters.get(enters_id[i]) == result:
                            if result == "⬛" or result == "🟥":
                                self.AC_DATA[enters_id[i]]['balance'] += (user_bet * 4)
                                self.AC_DATA_SAVE()
                                if result == "⬛" and winners == False:
                                    emb.set_thumbnail(url="https://www.roulettephysics.com/wp-content/uploads/2018/12/luck-839037_960_720.jpg")
                                    await message.edit(embed=emb)
                                elif result == "🟥" and winners == False:
                                    emb.set_thumbnail(url="https://www.gamblingsites.org/blog/wp-content/uploads/Roulette-Landing-Red-7.jpg")
                                    await message.edit(embed=emb)
                            elif result == "🟩":
                                self.AC_DATA[enters_id[i]]['balance'] += (user_bet * 14)
                                self.AC_DATA_SAVE()
                                if result == "🟩" and winners == False:
                                    emb.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/5/5d/13-02-27-spielbank-wiesbaden-by-RalfR-094.jpg")
                                    await message.edit(embed=emb)
                            name = self.enters_name.get(enters_id[i])
                            if tempint == False:
                                await ctx.send(f"`| A nyertes szin: {result} |`")
                                await ctx.send("`| A nyertesek:        |`")
                                tempint = True
                            await ctx.send(f":crown: `{name}` :crown:")
                            winners = True
                        elif winners == False:
                            if tempint == False and i < len(enters_id):
                                await ctx.send(f"`| A nyertes szin: {result} |`")
                                await ctx.send("`| A nyertesek:        |`")
                                tempint = True
                            if winners == False and i+1 == len(enters_id):
                                if result == "⬛" and winners == False:
                                    emb.set_thumbnail(url="https://www.roulettephysics.com/wp-content/uploads/2018/12/luck-839037_960_720.jpg")
                                    await message.edit(embed=emb)
                                elif result == "🟥" and winners == False:
                                    emb.set_thumbnail(url="https://www.gamblingsites.org/blog/wp-content/uploads/Roulette-Landing-Red-7.jpg")
                                    await message.edit(embed=emb)
                                elif result == "🟩" and winners == False:
                                    emb.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/5/5d/13-02-27-spielbank-wiesbaden-by-RalfR-094.jpg")
                                    await message.edit(embed=emb)
                                await ctx.send("Sajnos senki nem nyert, Több szerencsét legközelebbre!")
                                winners = True           

            self.enters.clear()
            self.enters_name.clear()

    # ROULETTE REACTION EVENT 
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        if user.id != self.client.user.id:
            if reaction.emoji == "\U0001f7e5" or reaction.emoji == "\U0001f7e9" or reaction.emoji == "⬛":
                self.enters[str(user.id)] = reaction.emoji
                self.enters_name[str(user.id)] = str(user.name)

            


def setup(client):
    client.add_cog(Casino(client))