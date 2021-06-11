import discord
import psutil
import os

from utils import default
from discord.ext import commands

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.name = self.config['name']
        self.version = self.config['version']
        self.guild = self.config['guild']
        self.process = psutil.Process(os.getpid())

    @commands.command(aliases=['stats', 'botinfo'])
    @commands.guild_only()
    async def about(self, ctx):
        """ Obtén algunas estadísticas del bot. """

        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)
        avgemojis = len(self.bot.emojis) / len(self.bot.guilds)

        before_ws = int(round(self.bot.latency * 1000, 1))

        embed = discord.Embed(color=self.config['blurple'])
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(
            name='Desarrollador',
            value=', '.join([str(self.bot.get_user(x)) for x in self.config['owners']]),
            inline=True
        )
        embed.add_field(name='Usuarios', value=f'{len(ctx.bot.users)} (~{avgmembers:.2f}/servidor)', inline=True)
        embed.add_field(name='Emojis', value=f'{len(ctx.bot.emojis)} (~{avgemojis:.2f}/servidor)', inline=True)
        embed.add_field(name='Librería', value=f'discord.py', inline=True)
        embed.add_field(name='Comandos', value=len([x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name='Memoria', value=f'{ramUsage:.2f} MB / 16GB', inline=True)
        embed.add_field(name='Latencia', value=f'Websocket: {before_ws}ms')
        await ctx.reply(content='ℹ Sobre **{0}** | **{1}**'.format(self.name, self.version), embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(BotInfo(bot))