import asyncio
import discord
from discord.ext import commands
from discord.channel import TextChannel, VoiceChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.member import Member, VoiceState
from discord.message import Message


class Role(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    @commands.has_permissions(kick_members=True)
    @commands.command(name='rolver')
    async def add_role(self, ctx: Context, member: Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.reply(f'**{member.mention} Kullanıcısına {role.mention} rolü verildi.**')

    @commands.has_permissions(kick_members=True)
    @commands.command(name='rolal')
    async def remove_role(self, ctx: Context, member: Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.reply(f'**{member.mention} Kullanıcısından {role.mention} rolü alındı.**')


def setup(client: Bot):
    client.add_cog(Role(client))
