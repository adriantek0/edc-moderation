import discord

from utils import permissions, default
from discord.ext import commands

class Moderación(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.name = self.config['name']
        self.version = self.config['version']
        self.guild = self.config['guild']

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """ Banea a un usuario del servidor. """

        try:
            await member.ban(reason=default.responsible(ctx.author, reason))
            await ctx.reply(content=':white_check_mark: **{0}** ha sido baneado del servidor.'.format(member), mention_author=False)
        except Exception as e:
            await ctx.reply(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(kick_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ Expulsa a un usuario del servidor. """

        try:
            await member.kick(reason=default.responsible(ctx.author, reason))
            await ctx.reply(content=':white_check_mark: **{0}** ha sido expulsado del servidor.'.format(member), mention_author=False)
        except Exception as e:
            await ctx.reply(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lockdown(self, ctx):
        """ Bloquea un canal a todos los miembros. """

        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.reply(content=f':white_check_mark: **{ctx.channel}** ha sido bloqueado para todos los usuarios.', mention_author=False)
        except Exception as e:
            await ctx.reply(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unlock(self, ctx):
        """ Desbloquea un canal a todos los miembros. """

        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.reply(content=f':white_check_mark: **{ctx.channel}** ha sido desbloqueado para todos los usuarios.', mention_author=False)
        except Exception as e:
            await ctx.reply(content=e, mention_author=False)

def setup(bot):
    bot.add_cog(Moderación(bot))