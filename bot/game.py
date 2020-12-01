import discord
from util.exception import NotAllowedCommand
from game.match import Match, Status
from discord.ext import commands



class Game(commands.Cog):
    """The commands for handle the game

            !captain - Set the user as captain of a team

       """
    def __init__(self, bot, starterHelper):
        self.bot = bot
        self.starterHelper = starterHelper

    def join_as_captain(self, guild, channel, member):
        if (guild.id,channel.id) in self.starterHelper.matches.keys():
            return self.starterHelper.matches[(guild.id, channel.id)].join_as_captain(member)
        else:
            raise NotAllowedCommand('Match not started')

    @commands.command()
    async def captain(self, ctx, *, member: discord.Member = None):
        """Set the user as captain of a team"""
        try:
            member = member or ctx.author
            res = self.join_as_captain(ctx.message.author.guild, ctx.message.channel, member)
            await ctx.send('{0.name} joined in {1} team~'.format(member, res))
            await ctx.send(self.starterHelper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)
