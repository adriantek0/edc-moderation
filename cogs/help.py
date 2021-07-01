import discord

from utils import default
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.name = self.config['name']
        self.version = self.config['version']
        self.guild = self.config['guild']

    @commands.command(aliases=['commands'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def help(self, ctx):
        """ Obtén la ayuda sobre el bot """

        embed = discord.Embed(color=self.config['blurple'])
        embed.set_author(name='Ejército de Chile', icon_url=self.bot.user.avatar_url)
        embed.add_field(name='Información', value='`about` - Obtén algunas estadísticas del bot\n`help` - Muestra esta lista de comandos\n`ranks` - Obtén la lista de rangos del grupo', inline=False)
        embed.add_field(name='Moderación', value='`ban` - Banea a un usuario del servidor\n`kick` - Expulsa a un usuario del servidor\n`lockdown` - Bloquea un canal a todos los miembros\n`mute` - Mutea a un usuario del servidor\n`unban` - Desbanea a un usuario del servidor\n`unlock` - Desbloquea un canal a todos los miembros\n`unmute` - Desmutea a un usuario del servidor', inline=False)
        embed.add_field(name='Roblox', value='`demote` - Demotea a un usuario del grupo\n`exile` - Exilia a un usuario del grupo\n`promote` - Promotea a un usuario del grupo\n`rango` - owo whats this?\n`setrank` - Establece un rango a un usuario del grupo\n`setrole` - Establece un role a un usuario del grupo\n`shout` - Envía un shout al grupo\n`whois` - Obtén la información de un usuario de Roblox', inline=False)
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Help(bot))