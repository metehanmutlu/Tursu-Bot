import os
import warnings
import aiohttp
from datetime import datetime
from settings import load_requirements
from database import Database

import discord
from discord.member import Member
from discord.ext import commands, tasks


config = load_requirements()

TOKEN = os.environ.get('TOKEN')
DB_TOKEN = os.environ.get('DB_TOKEN')
prefix = config['prefix']
warnings.filterwarnings("ignore", category=DeprecationWarning)
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
client.session = aiohttp.ClientSession()
client.remove_command('help')

db = Database(DB_TOKEN)
db.connect()
balanceIsUpdated = False


@client.event
async def on_ready():
    checkBalances.start()
    print('Bot is online....')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{prefix}help"))


@tasks.loop(minutes=5)
async def checkBalances():
    global balanceIsUpdated
    if not balanceIsUpdated:
        balances_db = db.getBalances()
        db.updateBalancesToJson(balances_db)
        balanceIsUpdated = True
        print('Update Successfully')
    else:
        balances_json = db.getBalancesFromJson()
        db.updateBalances(balances_json)
        print('Transfer Successfully')


@client.event
async def on_member_join(member: Member):
    balances = db.getBalancesFromJson()
    if str(member.id) not in balances:
        bonusTime = datetime.now().isoformat()
        balances[str(member.id)] = {
            'balance': 700,
            'bonus_time': bonusTime
        }
        db.updateBalancesToJson(balances)


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'**Loaded extension of {extension}**')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'**Unloaded extension of {extension}**')


if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.extensions
            client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
