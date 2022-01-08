import os
import json
import asyncio
import discord
from discord.ext import commands
from discord.channel import TextChannel, VoiceChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.member import Member, VoiceState
from discord.message import Message
from datetime import datetime, timedelta
from utils.randomColor import randColor


class Mute(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    async def timeout_user(self, *, user_id: int, guild_id: int, until):
        headers = {"Authorization": f"Bot {self.client.http.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        timeout = (datetime.utcnow() + timedelta(minutes=until)).isoformat()
        json = {'communication_disabled_until': timeout}
        async with self.client.session.patch(url, json=json, headers=headers) as session:
            if session.status in range(200, 299):
                return True
            return False

    async def untimeout_user(self, *, user_id: int, guild_id: int):
        headers = {"Authorization": f"Bot {self.client.http.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        timeout = (datetime.utcnow() + timedelta(minutes=0)).isoformat()
        json = {'communication_disabled_until': timeout}
        async with self.client.session.patch(url, json=json, headers=headers) as session:
            if session.status in range(200, 299):
                return True
            return False

    @commands.command(name='mute')
    async def mute(self, ctx: Context, member: Member, until: int):
        handshake = await self.timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=until)
        if handshake:
            return await ctx.send(f"**{ctx.author.mention} Kullanıcısı {until} dakika susturuldu.**")
        print('Mute Error')

    @commands.command(name='unmute')
    async def unmute(self, ctx: Context, member: Member):
        handshake = await self.untimeout_user(user_id=member.id, guild_id=ctx.guild.id)
        if handshake:
            return await ctx.send(f"**{ctx.author.mention} Kullanıcısının susturu kaldırıldı.**")
        print('Unmute Error')


def setup(client: Bot):
    client.add_cog(Mute(client))
