import discord
import numpy as np

from ro_py.client import Client
roblox = Client()

from utils import default
from discord.ext import commands
from discord.utils import escape_markdown
from ro_py.thumbnails import ThumbnailSize, ThumbnailType
from discord.ext.commands import has_permissions

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
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def shout(self, ctx, *, shout_text):
        group = await roblox.get_group(self.group)
        await group.shout(shout_text)
        await ctx.reply(content=':white_check_mark: Shout enviado.', mention_author=False)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def exile(self, ctx, username):
        group = await roblox.get_group(self.group)
        member = await group.get_member_by_username(username)
        await member.exile()
        await ctx.reply(content=':white_check_mark: Usuario exiliado.', mention_author=False)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def promote(self, ctx, username):
        group = await roblox.get_group(self.group)
        member = await group.get_member_by_username(username)
        await member.promote()
        await ctx.reply(content=':white_check_mark: Usuario promoteado.', mention_author=False)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def demote(self, ctx, username):
        group = await roblox.get_group(self.group)
        member = await group.get_member_by_username(username)
        await member.demote()
        await ctx.reply(content=':white_check_mark: Usuario demoteado.', mention_author=False)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def setrank(self, ctx, username, rank: int):
        group = await roblox.get_group(self.group)
        if 255 >= rank >= 1:
            member = await group.get_member_by_username(username)
            await member.setrole(rank)
            await ctx.reply(content=':white_check_mark: Usuario promoteado.', mention_author=False)
        else:
            await ctx.reply(content=':x: El rango debe ser al menos 1 y como máximo 255.', mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rango(self, ctx):
        group = await roblox.get_group(self.group)
        if ctx.guild:
            await ctx.reply(content=':x: Solo puedes ejecutar este comando en mis mensajes privados.', mention_author=False)
            return

        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        await ctx.reply(content=':white_small_square: Ingresa tu nombre de usuario en **Roblox.**', mention_author=False)
        username = await self.bot.wait_for('message', check=check)
        username = username.content
        
        try:
            user = await group.get_member_by_username(username)

            print(np.array(await group.get_members(limit=100)).join(' '))
            embed = discord.Embed(color=7506394)
            embed.description = np.array(await group.get_roles()).all()
            await ctx.reply(content=':white_small_square: ¿Este eres tú? (sí/no)', embed=embed, mention_author=False)

            confirm = await self.bot.wait_for('message', check=check)
            confirm = confirm.content

            if confirm == 'no':
                await ctx.reply(content=':x: Intenta ejecutar este comando de nuevo revisando que tu nombre de usuario esté bien escrito.', mention_author=False)
                return
        except Exception as e:
            await ctx.reply(content=f'```❌ {e}```', mention_author=False)
        

def setup(bot):
    bot.add_cog(Roblox(bot))