import discord
import numpy as np
from utils import default, permissions

from ro_py.client import Client
roblox = Client(default.config()['roblox'])

from discord.ext import commands
from discord.utils import escape_markdown
from ro_py.thumbnails import ThumbnailSize, ThumbnailType

class Roblox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.name = self.config['name']
        self.version = self.config['version']
        self.guild = self.config['guild']
        self.group = 4683210

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whois(self, ctx, username):
        """ Obtén la información de un usuario de Roblox """

        try:
            user = await roblox.get_user_by_username(username)
            embed = discord.Embed(color=7506394, title=f'Información de {user.name}')
            embed.add_field(name='Nombre de usuario', value=f'`{user.name}`')
            embed.add_field(name='Display name', value=f'`{user.display_name}`')
            embed.add_field(name='ID', value=f'`{str(user.id)}`')
            embed.add_field(name='Descripción', value=f'```{(escape_markdown(user.description or "No hay descripción."))}```')

            avatar_image = await user.thumbnails.get_avatar_image(
                shot_type=ThumbnailType.avatar_headshot,
                size=ThumbnailSize.size_420x420,
                is_circular=False
            )
            embed.set_thumbnail(url=avatar_image)
            await ctx.send(embed=embed, mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shout(self, ctx, *, shout_text):
        """ Envia un shout al grupo """

        if permissions.check_roblox(ctx.message.author) is False:
            return

        try:
            group = await roblox.get_group(self.group)
            await group.shout(shout_text)
            await ctx.send(content=':white_check_mark: Shout enviado.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def exile(self, ctx, username):
        """ Exilia a un usuario """

        if permissions.check_roblox(ctx.message.author) is False:
            return

        try:
            group = await roblox.get_group(self.group)
            member = await group.get_member_by_username(username)
            await member.exile()
            await ctx.send(content=':white_check_mark: Usuario exiliado correctamente.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def promote(self, ctx, username):
        """ Promotea a un usuario del grupo """

        if permissions.check_roblox(ctx.message.author) is False:
            return

        try:
            group = await roblox.get_group(self.group)
            member = await group.get_member_by_username(username)
            await member.promote()
            await ctx.send(content=':white_check_mark: Usuario promoteado correctamente.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def demote(self, ctx, username):
        """ Demotea a un usuario del grupo """

        if permissions.check_roblox(ctx.message.author) is False:
            return

        try:
            group = await roblox.get_group(self.group)
            member = await group.get_member_by_username(username)
            await member.demote()
            await ctx.send(content=':white_check_mark: Usuario demoteado correctamente.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setrank(self, ctx, username, rank: int):
        """ Establece un rango a un usuario del grupo """

        if permissions.check_roblox(ctx.message.author) is False:
            return

        try:
            group = await roblox.get_group(self.group)
            if 255 >= rank >= 1:
                member = await group.get_member_by_username(username)
                await member.setrole(rank)
                await ctx.send(content=':white_check_mark: Usuario actualizado correctamente.', mention_author=False)
            else:
                await ctx.send(content=':x: El rango debe ser al menos 1 y como máximo 255.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setrole(self, ctx, username, rank: int):
        """ Establece un rango a un usuario del grupo """

        if permissions.check_roblox(ctx.message.author) is False:
            return

        try:
            group = await roblox.get_group(self.group)
            if 255 >= rank >= 1:
                member = await group.get_member_by_username(username)
                await member.setrank(rank)
                await ctx.send(content=':white_check_mark: Usuario actualizado correctamente.', mention_author=False)
            else:
                await ctx.send(content=':x: El rango debe ser al menos 1 y como máximo 255.', mention_author=False)
        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ranks(self, ctx):
        """ Muestra la lista de rangos del grupo """

        try:
            group = await roblox.get_group(self.group)
            description = ''

            roles = await group.get_roles()
            for role in roles:
                description += f'`Rank {role.rank} (ID: {role.id})` **{role.name}** ({role.member_count} miembro{"" if role.member_count == 1 else "s"})\n'

            embed = discord.Embed(color=7506394, description=description)
            await ctx.send(content='ℹ Rangos del grupo', embed=embed, mention_author=False)

        except Exception as e:
            await ctx.send(content=f':x: Ocurrió un error.```{e}```')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rango(self, ctx):
        group = await roblox.get_group(self.group)
        if ctx.guild:
            await ctx.send(content=':x: Solo puedes ejecutar este comando en mis mensajes privados.', mention_author=False)
            return

        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        await ctx.send(content=':white_small_square: Ingresa tu nombre de usuario en **Roblox.**', mention_author=False)
        username = await self.bot.wait_for('message', check=check)
        username = username.content
        
        try:
            user = await group.get_member_by_username(username)

            print(np.array(await group.get_members(limit=100)).join(' '))
            embed = discord.Embed(color=7506394)
            embed.description = np.array(await group.get_roles()).all()
            await ctx.send(content=':white_small_square: ¿Este eres tú? (sí/no)', embed=embed, mention_author=False)

            confirm = await self.bot.wait_for('message', check=check)
            confirm = confirm.content

            if confirm == 'no':
                await ctx.send(content=':x: Intenta ejecutar este comando de nuevo revisando que tu nombre de usuario esté bien escrito.', mention_author=False)
                return
        except Exception as e:
            await ctx.send(content=f'```❌ {e}```', mention_author=False)
        
def setup(bot):
    bot.add_cog(Roblox(bot))