import discord

from utils import default
from discord.ext import commands
from discord.ext.commands import has_permissions

class Moderación(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.name = self.config['name']
        self.version = self.config['version']
        self.guild = self.config['guild']
        self.channel = self.bot.get_channel(852887722187685928)

    @commands.command()
    @commands.guild_only()
    @has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """ Banea a un usuario del servidor. """

        try:
            await member.ban(reason=default.responsible(ctx.author, reason))
            await ctx.reply(content=':white_check_mark: **{0}** ha sido baneado del servidor.'.format(member), mention_author=False)

            embed = discord.Embed()
            embed.set_author(name='Nuevo ban', icon_url=ctx.guild.icon_url)
            embed.add_field(name='Usuario', value=member, inline=True)
            embed.add_field(name='Moderador', value=ctx.author, inline=True)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            await self.channel.send(embed=embed)
        except Exception as e:
            await ctx.reply(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unban(self, ctx, *, member_id: int):
        """ Desbanea a un usuario del servidor. """

        try:
            await ctx.guild.unban(discord.Object(id=member_id))
            await ctx.reply(content=f':white_check_mark: **<@{member_id}>** ha sido desbaneado del servidor.', mention_author=False)

            embed = discord.Embed()
            embed.set_author(name='Nuevo unban', icon_url=ctx.guild.icon_url)
            embed.add_field(name='Usuario', value=member_id, inline=True)
            embed.add_field(name='Moderador', value=ctx.author, inline=True)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            await self.channel.send(embed=embed)
        except Exception as e:
            await ctx.reply(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(kick_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ Expulsa a un usuario del servidor. """

        try:
            await member.kick(reason=default.responsible(ctx.author, reason))
            await ctx.reply(content=':white_check_mark: **{0}** ha sido expulsado del servidor.'.format(member), mention_author=False)

            embed = discord.Embed()
            embed.set_author(name='Nuevo kick', icon_url=ctx.guild.icon_url)
            embed.add_field(name='Usuario', value=member, inline=True)
            embed.add_field(name='Moderador', value=ctx.author, inline=True)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            await self.channel.send(embed=embed)
        except Exception as e:
            await ctx.reply(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(manage_channels=True)
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
    @has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unlock(self, ctx):
        """ Desbloquea un canal a todos los miembros. """

        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.reply(content=f':white_check_mark: **{ctx.channel}** ha sido desbloqueado para todos los usuarios.', mention_author=False)
        except Exception as e:
            await ctx.reply(content=f':x: **{e}**', mention_author=False)

def setup(bot):
    bot.add_cog(Moderación(bot))