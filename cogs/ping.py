import asyncio
from discord.ext import commands
from discord.channel import TextChannel, VoiceChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.member import Member, VoiceState
from discord.message import Message


class Ping(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        elif message.content == 'hi':
            await message.reply('Hi dude!')

    @commands.command(name='ping')
    async def send_ping(self, ctx: Context):
        await ctx.reply('Pong!')


def setup(client: Bot):
    client.add_cog(Ping(client))
