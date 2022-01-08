import asyncio
import discord
from discord.ext import commands
from discord.channel import TextChannel, VoiceChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.member import Member, VoiceState
from discord.message import Message
from utils.randomColor import randColor


class Help(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    @commands.command(name='help')
    async def help(self, ctx: Context):
        prefix = '.'
        embed = discord.Embed()
        embed.color = randColor()
        embed.title = 'HELP'
        permissions: discord.Permissions = ctx.author.top_role.permissions
        embed.add_field(name=f'`{prefix}bonus`',
                        value='Saatlik bakiye bonusu almanı sağlar.', inline=False)
        embed.add_field(name=f'`{prefix}bakiye`',
                        value='Bakiyeni görüntüler.', inline=False)
        embed.add_field(name=f'`{prefix}zenginler`',
                        value='En çok bakiyeye sahip 10 kişiyi gösterir.', inline=False)
        embed.add_field(name=f'`{prefix}oyunlar`',
                        value='Oyunlar hakkında detaylı bilgi verir.', inline=False)
        if permissions.kick_members or permissions.administrator:
            embed.add_field(name=f'`{prefix}mute <@Kullanıcı / Kullanıcı ID> <Süre (Dakika)>`',
                            value=f'e.g => **{prefix}mute @mEDE 10**', inline=False)
            embed.add_field(name=f'`{prefix}unmute <@Kullanıcı / Kullanıcı ID>`',
                            value=f'e.g => **{prefix}unmute @mEDE**', inline=False)
            embed.add_field(name=f'`{prefix}ban <@Kullanıcı / Kullanıcı ID> <Sebep>`',
                            value=f'e.g => **{prefix}ban @mEDE Küfürden dolayı banlandı.**', inline=False)
            embed.add_field(name=f'`{prefix}unban <Kullanıcı#4444>`',
                            value=f'e.g => **{prefix}unban mEDE#4444**', inline=False)
            embed.add_field(name=f'`{prefix}kick <@Kullanıcı / Kullanıcı ID> <Sebep>`',
                            value=f'e.g => **{prefix}kick @mEDE Hakaretten dolayı atıldı.**', inline=False)
            embed.add_field(name=f'`{prefix}clear <Silinecek Mesaj Sayısı>`',
                            value=f'e.g => **{prefix}clear 10**', inline=False)
            embed.add_field(name=f'`{prefix}rolver <@Kullanıcı / Kullanıcı ID> <@Rol / Rol ID>`',
                            value=f'e.g => **{prefix}rolver @mEDE @Admin**', inline=False)
            embed.add_field(name=f'`{prefix}rolal <@Kullanıcı / Kullanıcı ID> <@Rol / Rol ID>`',
                            value=f'e.g => **{prefix}rolal @mEDE @Admin**', inline=False)
        # embed.add_field(name=f'`{prefix}`',
        #                 value='', inline=False)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


def setup(client: Bot):
    client.add_cog(Help(client))
