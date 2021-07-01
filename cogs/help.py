import discord
from time import time

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
        embed = discord.Embed(color=self.config['blurple'])
        embed.set_author(name='Ejército de Chile', icon_url=self.bot.user.avatar_url)
        embed.add_field(name='Información', value='`about` - Obtén algunas estadísticas del bot\n`help` - Muestra esta lista de comandos\n`ranks` - Obtén la lista de rangos del grupo', inline=False)
        embed.add_field(name='Moderación', value='`ban` - Banea a un usuario del servidor\n`kick` - Expulsa a un usuario del servidor\n`lockdown` - Bloquea un canal a todos los miembros\n`massban` - Banea múltiples usuarios del servidor\n`mute` - Mutea a un usuario del servidor\n`nickname` - Cambia el apodo a un usuario del servidor\n`prune` - Borra ciertos mensajes del servidor\n`unban` - Desbanea a un usuario del servidor\n`unlock` - Desbloquea un canal a todos los miembros\n`unmute` - Desmutea a un usuario del servidor', inline=False)
        embed.add_field(name='Roblox', value='`demote` - Demotea a un usuario del grupo\n`exile` - Exilia a un usuario del grupo\n`promote` - Promotea a un usuario del grupo\n`rango` - owo whats this?\n`setrank` - Establece un rango a un usuario del grupo\n`setrole` - Establece un role a un usuario del grupo\n`shout` - Envía un shout al grupo\n`whois` - Obtén la información de un usuario de Roblox', inline=False)
        await ctx.send(embed=embed)
    
    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif (not var_length):
                return f"<an empty {type(variable).__name__} iterable>"
        
        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (variable if (len(f"{variable}") <= 1000) else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>")
    
    def prepare(self, string):
        arr = string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command(pass_context=True, aliases=['eval', 'exec', 'evaluate'])
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        silent = ("-s" in code)
        
        code = self.prepare(code.replace("-s", ""))
        args = {
            "discord": discord,
            "imp": __import__,
            "this": self,
            "ctx": ctx
        }
        
        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, discord.Message):
                del args, code
                return
            
            await ctx.send(f"```py\n{self.resolve_variable(response)}````{type(response).__name__} | {(time() - a) / 1000} ms`")
        except Exception as e:
            await ctx.send(f"Error occurred:```\n{type(e).__name__}: {str(e)}```")
        
        del args, code, silent

def setup(bot):
    bot.add_cog(Help(bot))