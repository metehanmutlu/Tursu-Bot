import asyncio
import discord
from discord.ext import commands
from discord.channel import TextChannel, VoiceChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.member import Member, VoiceState
from discord.message import Message
from utils.randomColor import randColor


class Moderation(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx: Context, member: Member, *, reason: str = None):
        await member.ban(reason=reason)

        embed = discord.Embed(
            color=randColor(), title=f"Kullanıcı sunucudan yasaklandı!",
            description=f"**{ctx.author.mention}, {member.mention} Kullanıcısını sunucudan yasakladı**",
            timestamp=ctx.message.created_at
        )
        if reason != None:
            embed.add_field(name="Sebep", value=f"{reason}")
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='unban')
    async def unban(self, ctx: Context, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(color=randColor(), title="Kullanıcının yasağı kaldırıldı",
                                      description=f'**{user.mention} Kullanıcısının yasağı {ctx.author.mention} tarafından kaldırıldı**', timestamp=ctx.message.created_at)
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
                return

    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kick(self, ctx: Context, member: Member, *, reason: str = None):
        await member.kick(reason=reason)

        embed = discord.Embed(
            color=randColor(), title=f"Kullanıcı sunucudan atıldı!",
            description=f"**{ctx.author.mention}, {member.mention} Kullanıcısını sunucudan attı**",
            timestamp=ctx.message.created_at
        )
        if reason != None:
            embed.add_field(name="Sebep", value=f"{reason}")
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.command(name='clear')
    async def clear(self, ctx: Context, limit: int = 1):
        await ctx.channel.purge(limit=limit+1)


def setup(client: Bot):
    client.add_cog(Moderation(client))
