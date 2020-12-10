import discord
from util.exception import NotAllowedCommand
from game.match import ActionResult
from discord.ext import commands
from util.strings import get_string_bot as _


class Game(commands.Cog):
    """The commands for handle the game

            !captain - Set the user as captain of a team

       """

    def __init__(self, bot, game_helper):
        self.bot = bot
        self.game_helper = game_helper

    def join_as_master(self, guild, channel, member):
        if (guild.id, channel.id) in self.game_helper.matches.keys():
            return self.game_helper.matches[(guild.id, channel.id)].join_as_master(member)
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def show_word(self, guild, channel, member, word):
        if (guild.id, channel.id) in self.game_helper.matches.keys():
            return self.game_helper.matches[(guild.id, channel.id)].show(member, word)
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def pass_turn(self, guild, channel, member):
        if (guild.id, channel.id) in self.game_helper.matches.keys():
            return self.game_helper.matches[(guild.id, channel.id)].pass_turn(member)
        else:
            raise NotAllowedCommand(_('error_not_started'))

    async def send_images(self, ctx):
        await ctx.send('IMMAGINE')
        master_red = self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].team_red.master
        master_blue = self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].team_blue.master
        if master_red is not None:
            await master_red.send('IMMAGINE_PER_MASTER')
        if master_blue is not None:
            await master_blue.send('IMMAGINE_PER_MASTER')

    @commands.command()
    async def master(self, ctx, *, member: discord.Member = None):
        """Set the user as captain of a team"""
        try:
            member = member or ctx.author
            self.join_as_master(ctx.message.author.guild, ctx.message.channel, member)
            await ctx.send(_('user_joined', user=member.name))
            await ctx.send(self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].print_members())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def show(self, ctx, word, *, member: discord.Member = None):
        """Set the user as captain of a team"""
        try:
            member = member or ctx.author
            res = self.show_word(ctx.message.author.guild, ctx.message.channel, member, word)
            if res == ActionResult.FINISH:
                name = self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].winner.name
                await ctx.send(_('end_game', team=name))
            elif res == ActionResult.GUESS:
                await ctx.send(_('word_guessed'), word=word)
            else:
                await ctx.send(_('word_not_guessed'), word=word)
            await self.send_images(ctx)
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command(name='pass')
    async def _pass(self, ctx, *, member: discord.Member = None):
        try:
            member = member or ctx.author
            self.pass_turn(ctx.message.author.guild, ctx.message.channel, member)
        except NotAllowedCommand as err:
            await ctx.send(err.message)
