# bot.py
import os

import discord
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    # await guild.query_members()
    members = '\n - '.join([member.name for member in guild.members])
    print("len guild members:", len(guild.members))
    print(f'Guild Members:\n - {members}')

client.run(TOKEN)