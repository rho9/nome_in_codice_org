import discord
from util.exception import NotAllowedCommand
from game.match import ActionResult
from discord.ext import commands


class Game(commands.Cog):
    """The commands for handle the game

            !captain - Set the user as captain of a team

       """

    def __init__(self, bot, starter_helper):
        self.bot = bot
        self.starter_helper = starter_helper

    def join_as_master(self, guild, channel, member):
        if (guild.id, channel.id) in self.starter_helper.matches.keys():
            return self.starter_helper.matches[(guild.id, channel.id)].join_as_master(member)
        else:
            raise NotAllowedCommand('Match not started')

    def show_word(self, guild, channel, member, word):
        if (guild.id, channel.id) in self.starter_helper.matches.keys():
            return self.starter_helper.matches[(guild.id, channel.id)].show(member, word)
        else:
            raise NotAllowedCommand('Match not started')

    def pass_turn(self, guild, channel, member):
        if (guild.id, channel.id) in self.starter_helper.matches.keys():
            return self.starter_helper.matches[(guild.id, channel.id)].pass_turn(member)
        else:
            raise NotAllowedCommand('Match not started')

    async def send_immages(self, ctx):
        await ctx.send('IMMAGINE')
        master_red = self.starter_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].team_red.master
        master_blue = self.starter_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].team_blue.master
        await master_red.send('IMMAGINE')
        await master_blue.send('IMMAGINE')

    @commands.command()
    async def master(self, ctx, *, member: discord.Member = None):
        """Set the user as captain of a team"""
        try:
            member = member or ctx.author
            res = self.join_as_master(ctx.message.author.guild, ctx.message.channel, member)
            await ctx.send('{0.name} joined in {1} team~'.format(member, res))
            await ctx.send(self.starter_helper.print_status())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    # @commands.command()
    # async def show(self, ctx, *, member: discord.Member = None):
    #     """Set the user as captain of a team"""
    #     if (ctx.message.author.guild.id, ctx.message.channel.id) not in self.starterHelper.matches.keys() or\
    #             ((ctx.message.author.guild.id, ctx.message.channel.id) in self.starterHelper.matches.keys() and \
    #          self.starterHelper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].status == Status.PLAY):
    #         await ctx.send('It miss the word. Write !show [word]')
    #     else:
    #         await ctx.send('You can use this command only when a game is started. And it miss the word. Write !show [word]')

    @commands.command()
    async def show(self, ctx, word, *, member: discord.Member = None):
        """Set the user as captain of a team"""
        try:
            member = member or ctx.author
            res = self.show_word(ctx.message.author.guild, ctx.message.channel, member, word)
            if res == ActionResult.FINISH:
                name = self.starter_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].winner.name
                await ctx.send('game finished, team {} won.'.format(name))
            elif res == ActionResult.GUESS:
                await ctx.send('{} is correct, !show another word or !pass'.format(word))
            else:
                await ctx.send('{} isn\'t correct!'.format(word))
            await ctx.send(self.starter_helper.print_status())
            await self.send_immages(ctx)
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command(name='pass')
    async def _pass(self, ctx, *, member: discord.Member = None):
        try:
            member = member or ctx.author
            self.pass_turn(ctx.message.author.guild, ctx.message.channel, member)
        except NotAllowedCommand as err:
            await ctx.send(err.message)
