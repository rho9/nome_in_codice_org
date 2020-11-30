# bot.py
import os
import random
import discord
from discord.ext import commands
from bot.bot import Starter, GameHelper

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)
gameHelper = GameHelper()
bot.add_cog(Starter(bot, gameHelper))
bot.run(TOKEN)

