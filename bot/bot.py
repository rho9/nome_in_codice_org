import discord
from util.exception import NotAllowedCommand
from game.match import Match, Status
from discord.ext import commands

# This class store the matches for each server
class GameHelper:

    def __init__(self):
        self.matches = dict()

    def start(self, guild, channel):
        if (guild.id,channel.id) not in self.matches.keys():
            self.matches[(guild.id, channel.id)] = Match(guild, channel)
        self.matches[(guild.id, channel.id)].start()


    def join(self, guild_id, channel_id, member):
        if (guild_id,channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].join(member)
        else:
            raise NotAllowedCommand('The match is not started')

    def leave(self, guild_id, channel_id, member):
        if (guild_id,channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].leave(member)
        else:
            raise NotAllowedCommand('The match is not started')

    def play(self, guild_id, channel_id):
        if (guild_id,channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].play()
        else:
            raise NotAllowedCommand('The match is not started')

    def stop(self, guild_id, channel_id):
        if (guild_id,channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].stop()
        else:
            raise NotAllowedCommand('The match is not started')


    def print_status(self):
        s = ''
        for m in self.matches.keys():
            s += self.matches[m].print_status()
        return s



class Starter(commands.Cog):
    def __init__(self, bot, gameHelper):
        self.bot = bot
        self.gameHelper = gameHelper

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        await ctx.send('Hello {0.name}~'.format(member))

    @commands.command()
    async def start(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        print(ctx.message)
        try:
            self.gameHelper.start(ctx.message.author.guild, ctx.message.channel)
            member = member or ctx.author
            await ctx.send('Start {0.name}~'.format(member))
            await ctx.send(self.gameHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)


    @commands.command()
    async def join(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        print(ctx.message)
        try:
            self.gameHelper.join(ctx.message.guild.id, ctx.message.channel.id, ctx.author)
            member = member or ctx.author
            await ctx.send('Join {0.name}~'.format(member))
            await ctx.send(self.gameHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def leave(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        print(ctx.message)
        try:
            self.gameHelper.leave(ctx.message.guild.id, ctx.message.channel.id, ctx.author)
            member = member or ctx.author
            await ctx.send('leave {0.name}~'.format(member))
            await ctx.send(self.gameHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)


    @commands.command()
    async def play(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        print(ctx.message)
        try:
            self.gameHelper.play(ctx.message.guild.id, ctx.message.channel.id)
            member = member or ctx.author
            await ctx.send('play {0.name}~'.format(member))
            await ctx.send(self.gameHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def stop(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        print(ctx.message)
        try:
            self.gameHelper.stop(ctx.message.guild.id, ctx.message.channel.id)
            member = member or ctx.author
            await ctx.send('play {0.name}~'.format(member))
            await ctx.send(self.gameHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)


    @commands.command()
    async def status(self, ctx):
        """Says hello"""
        print(ctx.message)
        await ctx.send(self.gameHelper.print_status())