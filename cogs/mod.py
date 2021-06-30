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
        self.states = {}

    def are_overwrites_empty(self, overwrites):
        original = [p for p in iter(overwrites)]
        empty = [p for p in iter(discord.PermissionOverwrite())]
        return original == empty

    @commands.command()
    @commands.guild_only()
    @has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """ Banea a un usuario del servidor. """

        try:
            await member.ban(reason=default.responsible(ctx.author, reason))
            await ctx.send(content=':white_check_mark: **{0}** ha sido baneado del servidor.'.format(member), mention_author=False)

            embed = discord.Embed()
            embed.set_author(name='Nuevo ban', icon_url=ctx.guild.icon_url)
            embed.add_field(name='Usuario', value=member, inline=True)
            embed.add_field(name='Moderador', value=ctx.author, inline=True)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            await self.channel.send(embed=embed)
        except Exception as e:
            await ctx.send(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unban(self, ctx, *, member_id: int):
        """ Desbanea a un usuario del servidor. """

        try:
            await ctx.guild.unban(discord.Object(id=member_id))
            await ctx.send(content=f':white_check_mark: **<@{member_id}>** ha sido desbaneado del servidor.', mention_author=False)

            embed = discord.Embed()
            embed.set_author(name='Nuevo unban', icon_url=ctx.guild.icon_url)
            embed.add_field(name='Usuario', value=member_id, inline=True)
            embed.add_field(name='Moderador', value=ctx.author, inline=True)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            await self.channel.send(embed=embed)
        except Exception as e:
            await ctx.send(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(kick_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ Expulsa a un usuario del servidor. """

        try:
            await member.kick(reason=default.responsible(ctx.author, reason))
            await ctx.send(content=':white_check_mark: **{0}** ha sido expulsado del servidor.'.format(member), mention_author=False)

            embed = discord.Embed()
            embed.set_author(name='Nuevo kick', icon_url=ctx.guild.icon_url)
            embed.add_field(name='Usuario', value=member, inline=True)
            embed.add_field(name='Moderador', value=ctx.author, inline=True)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            await self.channel.send(embed=embed)
        except Exception as e:
            await ctx.send(content=e, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lockdown(self, ctx):
        """ Bloquea un canal a todos los miembros. """

        try:
            server = ctx.message.guild
            overwrites_everyone = ctx.message.channel.overwrites_for(server.default_role)
            overwrites_owner = ctx.message.channel.overwrites_for(server.role_hierarchy[0])
            if ctx.message.channel.id in self.states:
                await ctx.send(content='🔒 El canal ya está bloqueado. Utilice `unlock` para desbloquear.', mention_author=False)
                return
            states = []
            for a in ctx.message.guild.role_hierarchy:
                states.append([a, ctx.message.channel.overwrites_for(a).send_messages])
            self.states[ctx.message.channel.id] = states
            overwrites_owner.send_messages = True
            overwrites_everyone.send_messages = False
            await ctx.message.channel.set_permissions(server.default_role, overwrite=overwrites_everyone)
            await ctx.send(content='🔒 Canal bloqueado.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: {e}', mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unlock(self, ctx):
        """ Desbloquea un canal a todos los miembros. """

        try:
            if not ctx.message.channel.id in self.states:
                await ctx.send(content='🔓 El canal ya está desbloqueado.', mention_author=False)
                return
            for a in self.states[ctx.message.channel.id]:
                overwrites_a = ctx.message.channel.overwrites_for(a[0])
                overwrites_a.send_messages = a[1]
                await ctx.message.channel.set_permissions(a[0], overwrite=overwrites_a)
            self.states.pop(ctx.message.channel.id)
            await ctx.send(content='🔓 Canal desbloqueado.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: {e}', mention_author=False)
    
    @commands.command()
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member):
        if ctx.invoked_subcommand is None:
            if member and member != self.bot.user:
                failed = []
                channel_length = 0
                for channel in ctx.message.guild.channels:
                    if type(channel) != discord.channel.TextChannel:
                        continue
                    overwrites = channel.overwrites_for(member)
                    overwrites.send_messages = False
                    channel_length += 1
                    try:
                        await channel.set_permissions(member, overwrite=overwrites)
                    except discord.Forbidden:
                        failed.append(channel)
                if failed and len(failed) < channel_length:
                    await ctx.send(content=':white_check_mark: Usuario muteado en {}/{} canales.'.format(channel_length - len(failed), channel_length), mention_author=False)
                elif failed:
                    await ctx.send(content=':x: No se pudo silenciar al usuario. No hay suficientes permisos.', mention_author=False)
                else:
                    await ctx.send(content=':white_check_mark: Usuario muteado correctamente.', mention_author=False)
            else:
                await ctx.send(content=':x: No se pudo encontrar el usuario.', mention_author=False)

    @commands.command()
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member):
        if ctx.invoked_subcommand is None:
            if member and member != self.bot.user:
                failed = []
                channel_length = 0
                for channel in ctx.message.guild.channels:
                    if type(channel) != discord.channel.TextChannel:
                        continue
                    overwrites = channel.overwrites_for(member)
                    overwrites.send_messages = None
                    channel_length += 1
                    is_empty = self.are_overwrites_empty(overwrites)
                    try:
                        if not is_empty:
                            await channel.set_permissions(member, overwrite=overwrites)
                        else:
                            await channel.set_permissions(member, overwrite=None)
                        await channel.set_permissions(member, overwrite=overwrites)
                    except discord.Forbidden:
                        failed.append(channel)
                if failed and len(failed) < channel_length:
                    await ctx.send(content=':white_check_mark: Usuario desmuteado en {}/{} canales.'.format(channel_length - len(failed), channel_length), mention_author=False)
                elif failed:
                    await ctx.send(content=':x: No se pudo desmutear al usuario. No hay suficientes permisos.', mention_author=False)
                else:
                    await ctx.send(content=':white_check_mark: Usuario desmuteado correctamente.', mention_author=False)
            else:
                await ctx.send(content=':x: No se pudo encontrar el usuario.', mention_author=False)

def setup(bot):
    bot.add_cog(Moderación(bot))