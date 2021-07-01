import discord
import re

from utils import default, permissions
from discord.ext import commands

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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """ Banea a un usuario del servidor. """

        if permissions.check_mod(ctx.message.author) is False:
            return

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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ Expulsa a un usuario del servidor. """

        if permissions.check_mod(ctx.message.author) is False:
            return

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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lockdown(self, ctx):
        """ Bloquea un canal a todos los miembros. """

        if permissions.check_mod(ctx.message.author) is False:
            return

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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member):

        if permissions.check_mod(ctx.message.author) is False:
            return

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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unban(self, ctx, *, member_id: int):
        """ Desbanea a un usuario del servidor. """

        if permissions.check_mod(ctx.message.author) is False:
            return

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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unlock(self, ctx):
        """ Desbloquea un canal a todos los miembros. """

        if permissions.check_mod(ctx.message.author) is False:
            return

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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member):

        if permissions.check_mod(ctx.message.author) is False:
            return

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

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, nick: str = None):
        """ Cambia el apodo a un usuario del servidor """

        if permissions.check_mod(ctx.message.author) is False:
            return

        try:
            await member.edit(nick=nick)
            if nick is None:
                await ctx.send(content=f':white_check_mark: El apodo de **{member.name}\'s** ha sido reiniciado.')
                return
            await ctx.send(content=f':white_check_mark: El apodo de **{member.name}** fue cambiado a **{nick}**')
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error ejecutando el comando.\n```{e}```')

    @commands.command()
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def massban(self, ctx, *, members: discord.Member):
        """ Banea múltiples usuarios del servidor """

        if permissions.check_mod(ctx.message.author) is False:
            return

        description = '```diff\n'
        for member in members:
            try:
                await ctx.guild.ban(discord.Object(id=member.id))
                description += f'+ {member.name}#{member.discriminator} ha sido baneado correctamente.'
            except:
                description += f'- No he podido banear a {member.name}#{member.discriminator}.'
        
        description += '\n```'
        await ctx.send(content=description)
    
    @commands.group()
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.guild)
    async def prune(self, ctx):
        """ Borra mensajes del servidor. """

        if permissions.check_mod(ctx.message.author) is False:
            return

        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
    
    async def do_removal(self, ctx, limit, predicate, *, before=None, after=None, message=True):
        if limit > 2000:
            return await ctx.send(f':x: Demasiados mensajes a eliminar ({limit}/2000).')

        if not before:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
        except discord.Forbidden:
            return await ctx.send(':x: No tengo los permisos para borrar mensajes.')
        except discord.HTTPException as e:
            return await ctx.send(content=f':x: Ocurrió un error ejecutando el comando.\n```{e}```')

        deleted = len(deleted)
        if message is True:
            await ctx.send(f'🚮 Ha{"" if deleted == 1 else "n"} sido eliminado{"" if deleted == 1 else "s"} {deleted} mensaje{"" if deleted == 1 else "s"}.')
    
    @prune.command()
    async def embeds(self, ctx, search=100):
        """ Elimina los mensajes que tienen embeds """
        await self.do_removal(ctx, search, lambda e: len(e.embeds))

    @prune.command()
    async def files(self, ctx, search=100):
        """ Elimina los mensajes que tienen attachments """
        await self.do_removal(ctx, search, lambda e: len(e.attachments))

    @prune.command()
    async def mentions(self, ctx, search=100):
        """ Elimina los mensajes que tienen menciones """
        await self.do_removal(ctx, search, lambda e: len(e.mentions) or len(e.role_mentions))

    @prune.command()
    async def images(self, ctx, search=100):
        """ Elimina los mensajes que tienen embeds o attachments. """
        await self.do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @prune.command(name="all")
    async def _remove_all(self, ctx, search=100):
        """ Elimina todos los mensajes """
        await self.do_removal(ctx, search, lambda e: True)

    @prune.command()
    async def user(self, ctx, member: discord.Member, search=100):
        """ Elimina todos los mensajes de un usuario """
        await self.do_removal(ctx, search, lambda e: e.author == member)

    @prune.command()
    async def contains(self, ctx, *, substr: str):
        """Elimina todos los mensajes que contienen una subcadena.
        La subcadena debe tener al menos 3 caracteres.
        """
        if len(substr) < 3:
            await ctx.send(':x: La longitud de la subcadena debe ser de al menos 3 caracteres.')
        else:
            await self.do_removal(ctx, 100, lambda e: substr in e.content)

    @prune.command(name="bots")
    async def _bots(self, ctx, search=100, prefix=None):
        """ Elimina los mensajes de un usuario de bot y los mensajes con su prefijo opcional """

        getprefix = prefix if prefix else self.config['prefix']

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or m.content.startswith(tuple(getprefix))

        await self.do_removal(ctx, search, predicate)

    @prune.command(name="users")
    async def _users(self, ctx, prefix=None, search=100):
        """ Elimina solo los mensajes de los usuarios """

        def predicate(m):
            return m.author.bot is False

        await self.do_removal(ctx, search, predicate)

    @prune.command(name="emojis")
    async def _emojis(self, ctx, search=100):
        """ Elimina todos los mensajes que contienen emojis personalizados """
        custom_emoji = re.compile(r"<a?:(.*?):(\d{17,21})>|[\u263a-\U0001f645]")

        def predicate(m):
            return custom_emoji.search(m.content)

        await self.do_removal(ctx, search, predicate)

    @prune.command(name="reactions")
    async def _reactions(self, ctx, search=100):
        """ Elimina todas las reacciones de los mensajes que las tienen """

        if search > 2000:
            return await ctx.send(f':x: Demasiados mensajes ({search}/2000).')

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.send(f':white_check_mark: Se han eliminado {total_reactions} reacciones correctamente.')

def setup(bot):
    bot.add_cog(Moderación(bot))