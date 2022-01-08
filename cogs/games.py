import asyncio
import os
from datetime import datetime, timedelta
import random

from discord.guild import Guild
from settings import load_requirements
from utils.randomColor import randColor

import discord
from database import Database
from asyncio import sleep
from discord.channel import TextChannel, VoiceChannel
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.member import Member, VoiceState
from discord.message import Message
from discord.role import Role


config = load_requirements()


class Games(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client
        self.prefix = config['prefix']
        self.db = Database()
        # Slot Machine
        self.slot_list = []
        # Horse Racing
        self.bets = {}
        self.onRace = False

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        elif message.content == f'{config["prefix"]}slot':
            embed = discord.Embed(
                title="`SLOT`",
                colour=discord.Colour.gold()
            )
            embed.add_field(
                name="KULLANIM", value=f"`{config['prefix']}slot <Bahis>`", inline=False)
            embed.add_field(name="ORANLAR", value="**:first_place::first_place::grey_question: - 1x\n:gem::gem::grey_question: - 2x\n:100::100::grey_question: - 2x\n:first_place::first_place::first_place: - 3x\n:gem::gem::gem: - 3x\n:dollar::dollar::grey_question: - 3x\n:100::100::100: - 4x\n:moneybag::moneybag::grey_question: - 7x\n:dollar::dollar::dollar: - 7x\n:moneybag::moneybag::moneybag: - 15x**")
            await message.reply(embed=embed)
        elif message.content.lower() == 'merhaba':
            await message.reply('Merhaba')
        elif message.content.lower() == 'hello':
            await message.reply('Hello')
        elif message.content.lower() == 'hi':
            await message.reply('Hi')
        elif message.content.lower() == 'sa':
            await message.reply('AS')
        elif message.content.lower() == 'selam':
            await message.reply('Selam')

    @commands.command(name='bonus')
    async def give_bonus(self, ctx: Context):
        balances = self.db.getBalancesFromJson()
        member: Member = ctx.author
        guild: Guild = ctx.guild
        id = str(member.id)
        if id in balances:
            bonusTime = datetime.fromisoformat(balances[id]['bonus_time'])
            now = datetime.now()
            if bonusTime <= now:
                balances[id]['balance'] += 300
                delta = timedelta(hours=1)
                bonusTime = now + delta
                balances[id]['bonus_time'] = bonusTime.isoformat()
                self.db.updateBalancesToJson(balances)

                embed = discord.Embed(color=randColor())
                embed.title = 'Saatlik Bonus'
                embed.description = f'**{member.mention} Saatlik bonusu aldın\n\nYeni bakiyen: `{balances[id]["balance"]}`**'
                embed.timestamp = ctx.message.created_at
                embed.set_footer(text=guild.name, icon_url=guild.icon_url)
                await ctx.reply(embed=embed)
            else:
                remainingTime = int((bonusTime - now).seconds / 60)
                embed = discord.Embed(color=randColor())
                embed.title = 'Saatlik Bonus'
                embed.description = f'**{member.mention} Saatlik bonus almak için kalan süre: `{remainingTime}` dakika**'
                embed.timestamp = ctx.message.created_at
                embed.set_footer(text=guild.name, icon_url=guild.icon_url)
                await ctx.reply(embed=embed)
        else:
            now = datetime.now()
            delta = timedelta(hours=1)
            bonusTime = now + delta
            balances[str(member.id)] = {
                'balance': 300,
                'bonus_time': bonusTime.isoformat()
            }
            self.db.updateBalancesToJson(balances)

            embed = discord.Embed(color=randColor())
            embed.title = 'Saatlik Bonus'
            embed.description = f'**{member.mention} Saatlik bonusu aldın\n\nYeni bakiyen: `{balances[id]["balance"]}`**'
            embed.timestamp = ctx.message.created_at
            embed.set_footer(text=guild.name, icon_url=guild.icon_url)
            await ctx.reply(embed=embed)

    @commands.command(name='slot')
    async def slot_machine(self, ctx: Context, bet: int):
        balances = self.db.getBalancesFromJson()
        member: Member = ctx.author
        id = str(member.id)
        memberBalance = balances[id]['balance']
        if id not in self.slot_list:
            if id in balances:
                if memberBalance >= bet and memberBalance != 0 and bet > 0:
                    self.slot_list.append(id)
                    emojis = [":gem:", ":100:", ":first_place:",
                              ":dollar:", ":moneybag:"]
                    rates = [0.25, 0.2, 0.3, 0.15, 0.1]
                    win_lose_spin = [
                        "**--- KAYBETTİN ---**",
                        "**--- KAZANDIN ---**",
                        "**--- DÖNÜYOR ---**"
                    ]
                    slot_dict = {
                        "1": "<a:cycle:772229201448402965>",
                        "2": "<a:cycle:772229201448402965>",
                        "3": "<a:cycle:772229201448402965>"
                    }
                    slot_text = f"**--------------------\n| **{slot_dict['1']}** | **{slot_dict['2']}** | **{slot_dict['3']}** |\n--------------------\n**"
                    slot_embed = discord.Embed(
                        title="**Slot Makinesi**", colour=discord.Colour.green(), description=ctx.message.author.mention)
                    slot_embed.add_field(
                        name=slot_text, value=win_lose_spin[2])
                    embed_msg = await ctx.reply(embed=slot_embed)
                    await asyncio.sleep(1)

                    for x, y in slot_dict.items():
                        await asyncio.sleep(3)

                        random_emoji = random.choices(emojis, rates)
                        random_emoji = str(random_emoji)
                        random_emoji = random_emoji.replace("[", "")
                        random_emoji = random_emoji.replace("'", "")
                        random_emoji = random_emoji.replace("]", "")
                        slot_dict[x] = random_emoji
                        slot_text = f"**--------------------\n| **{slot_dict['1']}** | **{slot_dict['2']}** | **{slot_dict['3']}** |\n--------------------\n**"
                        new_slot_embed = discord.Embed(
                            title="**Slot Makinesi**", colour=discord.Colour.green(), description=ctx.message.author.mention)
                        new_slot_embed.add_field(
                            name=slot_text, value=win_lose_spin[2])
                        await embed_msg.edit(embed=new_slot_embed)
                    else:
                        if (slot_dict["1"] == ":gem:" and slot_dict["2"] == ":gem:" and slot_dict["3"] == ":gem:"):
                            profit = [True, 2]
                        elif (slot_dict["1"] == ":100:" and slot_dict["2"] == ":100:" and slot_dict["3"] == ":100:"):
                            profit = [True, 3]
                        elif (slot_dict["1"] == ":first_place:" and slot_dict["2"] == ":first_place:" and slot_dict["3"] == ":first_place:"):
                            profit = [True, 2]
                        elif (slot_dict["1"] == ":dollar:" and slot_dict["2"] == ":dollar:" and slot_dict["3"] == ":dollar:"):
                            profit = [True, 6]
                        elif (slot_dict["1"] == ":moneybag:" and slot_dict["2"] == ":moneybag:" and slot_dict["3"] == ":moneybag:"):
                            profit = [True, 14]
                        elif (slot_dict["1"] == ":gem:" and slot_dict["2"] == ":gem:"):
                            profit = [True, 1]
                        elif (slot_dict["3"] == ":gem:" and slot_dict["2"] == ":gem:"):
                            profit = [True, 1]
                        elif (slot_dict["1"] == ":100:" and slot_dict["2"] == ":100:"):
                            profit = [True, 1]
                        elif (slot_dict["3"] == ":100:" and slot_dict["2"] == ":100:"):
                            profit = [True, 1]
                        elif (slot_dict["1"] == ":first_place:" and slot_dict["2"] == ":first_place:"):
                            profit = [True, 0]
                        elif (slot_dict["3"] == ":first_place:" and slot_dict["2"] == ":first_place:"):
                            profit = [True, 0]
                        elif (slot_dict["1"] == ":dollar:" and slot_dict["2"] == ":dollar:"):
                            profit = [True, 2]
                        elif (slot_dict["3"] == ":dollar:" and slot_dict["2"] == ":dollar:"):
                            profit = [True, 2]
                        elif (slot_dict["1"] == ":moneybag:" and slot_dict["2"] == ":moneybag:"):
                            profit = [True, 6]
                        elif (slot_dict["3"] == ":moneybag:" and slot_dict["2"] == ":moneybag:"):
                            profit = [True, 6]
                        else:
                            profit = [False]

                        if profit[0]:
                            balances[id]['balance'] += bet*profit[1]
                            self.db.updateBalancesToJson(balances)
                            finish_embed = discord.Embed(
                                title="**Slot Makinesi**", colour=discord.Colour.green(), description=member.mention)
                            finish_embed.add_field(
                                name=slot_text, value=win_lose_spin[1], inline=False)
                            finish_embed.add_field(
                                name="Kazanç", value=f"**`+{bet*(profit[1]+1)}`**")
                            finish_embed.add_field(
                                name="Bakiye", value=f"**`{balances[id]['balance']}`**")
                            await embed_msg.edit(embed=finish_embed)
                            self.slot_list.remove(id)
                        else:
                            balances[id]['balance'] -= bet
                            self.db.updateBalancesToJson(balances)
                            finish_embed = discord.Embed(
                                title="**Slot Makinesi**", colour=discord.Colour.red(), description=member.mention)
                            finish_embed.add_field(
                                name=slot_text, value=win_lose_spin[0], inline=False)
                            finish_embed.add_field(
                                name="Kazanç", value=f"**`-{bet}`**")
                            finish_embed.add_field(
                                name="Bakiye", value=f"**`{balances[id]['balance']}`**")
                            await embed_msg.edit(embed=finish_embed)
                            self.slot_list.remove(id)
                else:
                    await ctx.reply(f'**{member.mention} Bakiyen Yetersiz**')

    @commands.command(name='atbahis')
    async def horse_betting(self, ctx: Context, horse: int, bet: int):
        if not self.onRace:
            member: Member = ctx.author
            if str(member.id) not in self.bets:
                if 1 <= horse <= 5:
                    balances: dict = self.db.getBalancesFromJson()
                    if str(member.id) in balances:
                        memberBalance: int = balances[str(
                            member.id)]['balance']
                        if memberBalance >= bet and memberBalance != 0 and bet > 0:
                            self.bets[str(member.id)] = {
                                'bet': bet,
                                'horse': horse
                            }
                            balances[str(member.id)]['balance'] -= bet
                            self.db.updateBalancesToJson(balances)
                            await ctx.reply(f'**{member.mention} Bahisin yatırıldı, Herkesin bahis yatırma işlemi bittiğinde `{config["prefix"]}yarışbaşlat` yazarak başlatınız.**')
                        else:
                            await ctx.reply(f'**{member.mention} Yetersiz bakiye.**')
                else:
                    await ctx.reply(f'**{ctx.author.mention} 1 - 5 Arasında bir at numarası seçmen gerekir.**')
            else:
                await ctx.reply(f'**Zaten bahis yaptın.**')
        else:
            print('Devam eden yarış bulunmakta.')

    @commands.command(name='yarışbaşlat')
    async def start_race(self, ctx: Context):
        channel: TextChannel = ctx.message.channel
        if not self.onRace:
            if 'at' in channel.name:
                race_text = ':checkered_flag:---------------:horse_racing:\n \n' * 5
                horse_roads = race_text.split(':checkered_flag:')[1::]
                race_message = await ctx.send(race_text)
                self.onRace = True

                while ('-' in horse_roads[0]) and ('-' in horse_roads[1]) and ('-' in horse_roads[2]) and ('-' in horse_roads[3]) and ('-' in horse_roads[4]):
                    random_values = random.sample(
                        horse_roads, random.randint(1, 2))
                    value = random.randint(1, 2)
                    if len(random_values) == 2:
                        if set(random_values) == {horse_roads[0], horse_roads[1]}:
                            horse_roads[0] = horse_roads[0].replace(
                                '-', '', value)
                            horse_roads[1] = horse_roads[1].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[0], horse_roads[2]}:
                            horse_roads[0] = horse_roads[0].replace(
                                '-', '', value)
                            horse_roads[2] = horse_roads[2].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[0], horse_roads[3]}:
                            horse_roads[0] = horse_roads[0].replace(
                                '-', '', value)
                            horse_roads[3] = horse_roads[3].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[0], horse_roads[4]}:
                            horse_roads[0] = horse_roads[0].replace(
                                '-', '', value)
                            horse_roads[4] = horse_roads[4].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[1], horse_roads[2]}:
                            horse_roads[1] = horse_roads[1].replace(
                                '-', '', value)
                            horse_roads[2] = horse_roads[2].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[1], horse_roads[3]}:
                            horse_roads[1] = horse_roads[1].replace(
                                '-', '', value)
                            horse_roads[3] = horse_roads[3].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[1], horse_roads[4]}:
                            horse_roads[1] = horse_roads[1].replace(
                                '-', '', value)
                            horse_roads[4] = horse_roads[4].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[2], horse_roads[3]}:
                            horse_roads[2] = horse_roads[2].replace(
                                '-', '', value)
                            horse_roads[3] = horse_roads[3].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[2], horse_roads[4]}:
                            horse_roads[2] = horse_roads[2].replace(
                                '-', '', value)
                            horse_roads[4] = horse_roads[4].replace(
                                '-', '', value)
                        elif set(random_values) == {horse_roads[3], horse_roads[4]}:
                            horse_roads[3] = horse_roads[3].replace(
                                '-', '', value)
                            horse_roads[4] = horse_roads[4].replace(
                                '-', '', value)

                    elif len(random_values) == 1:
                        if random_values[0] == horse_roads[0]:
                            horse_roads[0] = horse_roads[0].replace(
                                '-', '', value)
                        elif random_values[0] == horse_roads[1]:
                            horse_roads[1] = horse_roads[1].replace(
                                '-', '', value)
                        elif random_values[0] == horse_roads[2]:
                            horse_roads[2] = horse_roads[2].replace(
                                '-', '', value)
                        elif random_values[0] == horse_roads[3]:
                            horse_roads[3] = horse_roads[3].replace(
                                '-', '', value)
                        elif random_values[0] == horse_roads[4]:
                            horse_roads[4] = horse_roads[4].replace(
                                '-', '', value)

                    await asyncio.sleep(0.5)
                    await race_message.edit(content=f':checkered_flag:{horse_roads[0]}:checkered_flag:{horse_roads[1]}:checkered_flag:{horse_roads[2]}:checkered_flag:{horse_roads[3]}:checkered_flag:{horse_roads[4]}')
                else:
                    embed = discord.Embed(color=discord.Colour.dark_green())
                    embed.title = 'AT BAHİS SONUÇLARI'
                    embed.set_footer(text=ctx.guild.name,
                                     icon_url=ctx.guild.icon_url)
                    if '-' not in horse_roads[0]:
                        embed.description = '**Kazanan 1. At**'
                        for id, data in self.bets.items():
                            member = discord.utils.find(
                                lambda m: m.id == int(id), ctx.guild.members)
                            if data['horse'] == 1:
                                embed.add_field(
                                    name=member, value=f'`+{data["bet"] * 5}`', inline=False)
                                balances = self.db.getBalancesFromJson()
                                balances[str(member.id)
                                         ]['balance'] += data['bet'] * 5
                                self.db.updateBalancesToJson(balances)
                            else:
                                embed.add_field(
                                    name=member, value=f'`-{data["bet"]}`', inline=False)
                        else:
                            await ctx.send(embed=embed)

                    elif '-' not in horse_roads[1]:
                        embed.description = '**Kazanan 2. At**'
                        for id, data in self.bets.items():
                            member = discord.utils.find(
                                lambda m: m.id == int(id), ctx.guild.members)
                            if data['horse'] == 2:
                                embed.add_field(
                                    name=member, value=f'`+{data["bet"] * 5}`', inline=False)
                                balances = self.db.getBalancesFromJson()
                                balances[str(member.id)
                                         ]['balance'] += data['bet'] * 5
                                self.db.updateBalancesToJson(balances)
                            else:
                                embed.add_field(
                                    name=member, value=f'`-{data["bet"]}`', inline=False)
                        else:
                            await ctx.send(embed=embed)

                    elif '-' not in horse_roads[2]:
                        embed.description = '**Kazanan 3. At**'
                        for id, data in self.bets.items():
                            member = discord.utils.find(
                                lambda m: m.id == int(id), ctx.guild.members)
                            if data['horse'] == 3:
                                embed.add_field(
                                    name=member, value=f'`+{data["bet"] * 5}`', inline=False)
                                balances = self.db.getBalancesFromJson()
                                balances[str(member.id)
                                         ]['balance'] += data['bet'] * 5
                                self.db.updateBalancesToJson(balances)
                            else:
                                embed.add_field(
                                    name=member, value=f'`-{data["bet"]}`', inline=False)
                        else:
                            await ctx.send(embed=embed)

                    elif '-' not in horse_roads[3]:
                        embed.description = '**Kazanan 4. At**'
                        for id, data in self.bets.items():
                            member = discord.utils.find(
                                lambda m: m.id == int(id), ctx.guild.members)
                            if data['horse'] == 4:
                                embed.add_field(
                                    name=member, value=f'`+{data["bet"] * 5}`', inline=False)
                                balances = self.db.getBalancesFromJson()
                                balances[str(member.id)
                                         ]['balance'] += data['bet'] * 5
                                self.db.updateBalancesToJson(balances)
                            else:
                                embed.add_field(
                                    name=member, value=f'`-{data["bet"]}`', inline=False)
                        else:
                            await ctx.send(embed=embed)

                    elif '-' not in horse_roads[4]:
                        embed.description = '**Kazanan 5. At**'
                        for id, data in self.bets.items():
                            member = discord.utils.find(
                                lambda m: m.id == int(id), ctx.guild.members)
                            if data['horse'] == 5:
                                embed.add_field(
                                    name=member.mention, value=f'`+{data["bet"] * 5}`', inline=False)
                                balances = self.db.getBalancesFromJson()
                                balances[str(member.id)
                                         ]['balance'] += data['bet'] * 5
                                self.db.updateBalancesToJson(balances)
                            else:
                                embed.add_field(
                                    name=member.mention, value=f'`-{data["bet"]}`', inline=False)
                        else:
                            await ctx.send(embed=embed)

                    self.onRace = False
                    self.bets = {}
            else:
                horse_channel = discord.utils.find(
                    lambda c: 'at-yarışı' in c.name, ctx.guild.text_channels)
                await ctx.send(f'**Komutu {horse_channel.mention} kanalında kullanınız.**')

    @commands.command(name='bakiye')
    async def balance(self, ctx: Context):
        balances = self.db.getBalancesFromJson()
        if str(ctx.author.id) in balances:
            memberBalance = balances[str(ctx.author.id)]['balance']
            embed = discord.Embed(color=randColor())
            embed.title = '`BAKİYE`'
            embed.description = f'**{ctx.author.mention}: `{memberBalance}`**'
            embed.timestamp = ctx.message.created_at
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f'**`{self.prefix}bonus` Yazarak bonus bakiye alabilirsin.**')

    @commands.command(name='zenginler')
    async def rich(self, ctx: Context):
        balances = self.db.getBalancesFromJson()
        embed = discord.Embed(color=randColor())
        embed.title = '`ZENGİNLER`'
        descriptionText = '**'
        members = []
        for i, member in enumerate(balances):
            members.append((balances[member]['balance'], int(member)))
            if i == 9:
                break

        members.sort(reverse=True)
        for i, id in enumerate(members):
            member = discord.utils.find(
                lambda m: m.id == int(id[1]), ctx.guild.members)
            if member is not None:
                descriptionText += f'{i+1}. {member.mention}: `{id[0]}`\n'
        else:
            descriptionText += '**'
            embed.description = descriptionText
            for i, member in enumerate(balances):
                if ctx.author.id == int(member):
                    embed.set_footer(text=f'Sizin sıranız • {i+1}')
                    break

            await ctx.reply(embed=embed)
        # sort = 0
        # sorted_balance = sorted(
        #     balances.items(), key=lambda x: x[1], reverse=True)
        # for x, y in sorted_balance:
        #     print(x, y)
        #     sort += 1
        #     descriptionText += f'{sort}. {x}: `{y["balance"]}`\n'
        #     # embed.add_field(name=f"{sort}. {member}", value=f"`{y['balance']}`", inline=False)
        #     if sort == 10:
        #         descriptionText += '**'
        #         embed.description = descriptionText
        #         break

    @commands.command(name='oyunlar')
    async def show_games(self, ctx: Context):
        embed = discord.Embed(
            title="**OYUNLAR**\n",
            colour=randColor(),
            description=f"Saatlik bonus almak için `{config['prefix']}bonus` komutunu kullanabilirsin."
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/766388809142632498/766390509572456468/cons.png")
        embed.add_field(name="Slot Makinesi",
                        value=f"`{config['prefix']}slot` `|` `{config['prefix']}slot <Bahis>` Yatırmak istediğin tutarı gir ve makineyi çalıştır eğer şanslıysan kazanırsın.", inline=False)
        embed.add_field(name="At Yarışı",
                        value=f"`{config['prefix']}atbahis <1 - 5 Arasında bir at numarası>` Eğer atın kazanırsa yatırdığın miktarın 3 katını kazanırsın.", inline=False)
        await ctx.reply(embed=embed)


def setup(client: Bot):
    client.add_cog(Games(client))
