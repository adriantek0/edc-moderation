import discord

from utils import default
from discord.ext import commands

owners = default.config()['owners']

async def check_permissions(ctx, perms, *, check=all):
    """ Checks if author has permissions to a permission """
    if ctx.author.id in owners:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def has_permissions(*, check=all, **perms):
    """ discord.Commands method to check if author has permissions """
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)