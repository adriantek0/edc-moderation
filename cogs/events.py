import discord 

from utils import default
from discord.ext import commands
from discord.ext.commands import errors

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Game(
                name='ROBLOX'
            ),
            status=discord.Status.idle
        )
        print(f'{self.bot.user} ready!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)

        if isinstance(err, errors.CommandOnCooldown):
            await ctx.send(content=f':x: Weon, el comando está en cooldown, ¿cachai?. Vuelve a ejecutarlo en **{err.retry_after:.2f}s**', mention_author=False)

def setup(bot):
    bot.add_cog(Events(bot))