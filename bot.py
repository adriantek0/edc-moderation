from discord.ext import commands
import discord
import os
from utils import default
config = default.config()

bot = commands.Bot(
    command_prefix=config['prefix'],
    prefix=config['prefix'],
    owner_ids=config['owners'],
    intents=discord.Intents(
        guilds=True,
        members=True,
        messages=True,
        reactions=True,
    ),
    case_insensitive=True
)

bot.remove_command('help')

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        name = file[:-3]
        try:
           bot.load_extension(f'cogs.{name}')
        except Exception as e:
            print(f'Error loading {name}: {e}')

try:
    bot.run(config['token'])
except Exception as e:
    print(f'Error when logging in: {e}')