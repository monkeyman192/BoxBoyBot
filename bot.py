import discord
from discord.ext import commands
import random
import asyncio
from srcom_get import GetData, GetRandom

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@asyncio.coroutine
def joined(member : discord.Member):
    """Says when a member joined."""
    yield from bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.command()
@asyncio.coroutine
def wr(level_id : str, *costume : str):
    """world record data for the requested level code."""
    data = GetData(level_id, *costume)
    yield from bot.say(data.return_data)

@bot.command()
@asyncio.coroutine
def rand():
    """Returns a random level to play."""
    data = GetRandom()
    yield from bot.say(data)

bot.run('MzE2OTIxODQ5MTI2NzE1Mzk1.DAcUbA.D6EOv_8zFzoyTp9PN9bK4H4LbO8')
