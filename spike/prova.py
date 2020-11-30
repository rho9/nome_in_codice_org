# bot.py
import os
import random
import discord
from discord.ext import commands

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='salutami')
async def salutami(ctx):
    await ctx.send('ciao cane')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    # await guild.query_members()
    members = '\n - '.join([member.name for member in guild.members])
    print("len guild members:", len(guild.members))
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name='create-channel')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='fiero'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


# ESEMPIO per gestire tutti i messaggi
# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#
#     await message.channel.send("ciao")

bot.run(TOKEN)