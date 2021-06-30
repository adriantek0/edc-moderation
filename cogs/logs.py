import discord 

from utils import default
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.content is not None:
            embed = discord.Embed(color=discord.Color.red())
            embed.set_author(name='Un mensaje ha sido borrado', icon_url=message.guild.icon_url)
            embed.add_field(name='Autor', value=message.author, inline=True)
            embed.add_field(name='Contenido', value=message.content, inline=True)
            embed.add_field(name='Mensaje', value=message.id, inline=True)
            embed.set_footer(text=f'{message.author} ({message.author.id})', icon_url=message.author.avatar_url)

            channel = self.bot.get_channel(692164258083110952)
            await channel.send(embed=embed)
            return
        else:
            embed = discord.Embed(color=discord.Color.red())
            embed.set_author(name='Un mensaje ha sido borrado', icon_url=message.guild.icon_url)
            embed.add_field(name='Autor', value=message.author, inline=True)
            embed.add_field(name='Mensaje', value=message.id, inline=True)
            embed.set_footer(text=f'{message.author} ({message.author.id})', icon_url=message.author.avatar_url)

            for attachment in message.attachments:
                embed.add_field(name='Attachment', value=f'[Click aquí]({attachment.proxy_url})')

            channel = self.bot.get_channel(692164258083110952)
            await channel.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content and after.content is not None:
            embed = discord.Embed(color=discord.Color.gold())
            embed.set_author(name='Un mensaje ha sido editado', icon_url=after.guild.icon_url)
            embed.add_field(name='Autor', value=after.author, inline=True)
            embed.add_field(name='Viejo contenido', value=before.content, inline=True)
            embed.add_field(name='Nuevo contenido', value=after.content, inline=True)
            embed.add_field(name='Mensaje', value=after.id, inline=True)
            embed.set_footer(text=f'{after.author} ({after.author.id})', icon_url=after.author.avatar_url)

            channel = self.bot.get_channel(692164258083110952)
            await channel.send(embed=embed)
            return
        elif before.content is None:
            embed = discord.Embed(color=discord.Color.gold())
            embed.set_author(name='Un mensaje ha sido editado', icon_url=after.guild.icon_url)
            embed.add_field(name='Autor', value=after.author, inline=True)
            embed.add_field(name='Nuevo contenido', value=after.content, inline=True)
            embed.add_field(name='Mensaje', value=after.id, inline=True)
            embed.set_footer(text=f'{after.author} ({after.author.id})', icon_url=after.author.avatar_url)

            for attachment in before.attachments:
                embed.add_field(name='Viejo contenido (attachment)', value=f'[Click aquí]({attachment.proxy_url})', inline=True)

            channel = self.bot.get_channel(692164258083110952)
            await channel.send(embed=embed)
            return
        elif after.content is None:
            embed = discord.Embed(color=discord.Color.gold())
            embed.set_author(name='Un mensaje ha sido editado', icon_url=after.guild.icon_url)
            embed.add_field(name='Autor', value=after.author, inline=True)
            embed.add_field(name='Viejo contenido', value=before.content, inline=True)
            embed.add_field(name='Mensaje', value=after.id, inline=True)
            embed.set_footer(text=f'{after.author} ({after.author.id})', icon_url=after.author.avatar_url)

            for attachment in after.attachments:
                embed.add_field(name='Nuevo contenido (attachment)', value=f'[Click aquí]({attachment.proxy_url})', inline=True)

            channel = self.bot.get_channel(692164258083110952)
            await channel.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message

        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name='Reacción añadida', icon_url=message.guild.icon_url)
        embed.add_field(name='Autor del mensaje', value=f'{message.author} ({message.author.id})', inline=True)
        embed.add_field(name='Reacción', value=reaction, inline=True)
        embed.set_footer(text=f'{user} ({user.id})', icon_url=user.avatar_url)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        message = reaction.message

        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name='Reacción removida', icon_url=message.guild.icon_url)
        embed.add_field(name='Autor del mensaje', value=f'{message.author} ({message.author.id})', inline=True)
        embed.add_field(name='Reacción', value=reaction, inline=True)
        embed.set_footer(text=f'{user} ({user.id})', icon_url=user.avatar_url)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name='Canal eliminado', icon_url=channel.guild.icon_url)
        embed.add_field(name='Nombre', value=channel.name, inline=True)
        embed.add_field(name='ID', value=channel.id, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name='Canal creado', icon_url=channel.guild.icon_url)
        embed.add_field(name='Nombre', value=channel.name, inline=True)
        embed.add_field(name='ID', value=channel.id, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name='Un usuario ha entrado al servidor', icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Nombre', value=member, inline=True)
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Creación', value=member.created_at, inline=True)
        embed.add_field(name='Color', value=member.colour, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
        channel2 = self.bot.get_channel(732772579487514624)
        await channel2.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name='Un usuario ha salido del servidor', icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Nombre', value=member, inline=True)
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Creación', value=member.created_at, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
        channel2 = self.bot.get_channel(732772579487514624)
        await channel2.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name='Un role ha sido creado', icon_url=role.guild.icon_url)
        embed.add_field(name='Nombre', value=role.name, inline=True)
        embed.add_field(name='ID', value=role.id, inline=True)
        embed.add_field(name='Hoist', value=role.hoist, inline=True)
        embed.add_field(name='Posición', value=role.position, inline=True)
        embed.add_field(name='Administrado', value=role.managed, inline=True)
        embed.add_field(name='Mencionable', value=role.mentionable, inline=True)
        embed.add_field(name='Color', value=role.color, inline=True)
        embed.add_field(name='Mención', value=role.mention, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name='Un role ha sido eliminado', icon_url=role.guild.icon_url)
        embed.add_field(name='Nombre', value=role.name, inline=True)
        embed.add_field(name='ID', value=role.id, inline=True)
        embed.add_field(name='Hoist', value=role.hoist, inline=True)
        embed.add_field(name='Administrado', value=role.managed, inline=True)
        embed.add_field(name='Mencionable', value=role.mentionable, inline=True)
        embed.add_field(name='Color', value=role.color, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name='Un usuario ha sido baneado', icon_url=guild.icon_url)
        embed.add_field(name='Nombre', value=user.name, inline=True)
        embed.add_field(name='ID', value=user.id, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name='Un usuario ha sido desbaneado', icon_url=guild.icon_url)
        embed.add_field(name='Nombre', value=user.name, inline=True)
        embed.add_field(name='ID', value=user.id, inline=True)

        channel = self.bot.get_channel(692164258083110952)
        await channel.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Logs(bot))