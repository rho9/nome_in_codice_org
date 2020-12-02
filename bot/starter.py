import discord
from util.exception import NotAllowedCommand
from game.match import Match, Status
from discord.ext import commands

# This class store the matches for each server
class StarterHelper:
    """A class to store the matches for each server and channel. It helps also to change the status.

           """
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

    def play(self, guild_id, channel_id, tag):
        if (guild_id,channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].play(tag)
        else:
            raise NotAllowedCommand('The match is not started')

    def stop(self, guild_id, channel_id):
        if (guild_id,channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].stop()
        else:
            raise NotAllowedCommand('The match is not started')


    def print_status(self):
        """print the status

            """
        s = 'Match'
        for m in self.matches.keys():
            s += self.matches[m].print_status()
        return s



class Starter(commands.Cog):
    """The commands for handle the start, join and stop of a game

        !start - start a game in which player can join with join command.

        !join - Join in the game. Allowed only if the game is JOINABLE

        !leave - leave the game. Allowed only if the game is JOINABLE

        !play - The game start and is not joinable anymore

        !stop - Stop the game

        !status - Send the status
       """

    def __init__(self, bot, gameHelper):
        self.bot = bot
        self.gameHelper = gameHelper

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """ Says hello

            """
        member = member or ctx.author
        await ctx.send('Hello {0.name}~'.format(member))

    @commands.command()
    async def start(self, ctx, *, member: discord.Member = None):
        """ start a game in which player can join with join command.

        """
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
        """ Join in the game. Allowed only if the game is JOINABLE

        """
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
        """leave the game. Allowed only if the game is JOINABLE

        """
        print(ctx.message)
        try:
            self.gameHelper.leave(ctx.message.guild.id, ctx.message.channel.id, ctx.author)
            member = member or ctx.author
            await ctx.send('leave {0.name}~'.format(member))
            await ctx.send(self.gameHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)


    @commands.command()
    async def play(self, ctx, tag, *, member: discord.Member = None):
        """ The game start and is not joinable anymore

        """
        print(ctx.message)
        try:
            self.gameHelper.play(ctx.message.guild.id, ctx.message.channel.id, tag)
            member = member or ctx.author
            await ctx.send('play {0.name} tag {1}~'.format(member, tag))
            await ctx.send(self.gameHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def stop(self, ctx, *, member: discord.Member = None):
        """ Stop the game

            """
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
        """ send the status

        """
        print(ctx.message)
        await ctx.send(self.gameHelper.print_status())

