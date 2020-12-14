import discord
from util.exception import NotAllowedCommand
from game.match import ActionResult
from discord.ext import commands
from game.image_generator import ImageGenerator
from util.strings import get_string_bot as _


class Game(commands.Cog):
    """The commands for handle the game

            !captain - Set the user as captain of a team

       """

    def __init__(self, bot, game_helper):
        self.bot = bot
        self.game_helper = game_helper
        self.image_generator = ImageGenerator()

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
        words = self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].grid_table.words
        next_team = self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].current_turn.name
        spies_image = [discord.File(ImageGenerator().generate(words, False))]
        await ctx.send(_('turn', team=next_team),files=spies_image)
        master_red = self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].team_red.master
        master_blue = self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].team_blue.master
        if master_red is not None:
            masters_image = [discord.File(ImageGenerator().generate(words, True))]
            await master_red.send(files=masters_image)
        if master_blue is not None:
            masters_image = [discord.File(ImageGenerator().generate(words, True))]
            await master_blue.send(files=masters_image)

    @commands.command()
    async def master(self, ctx, *, member: discord.Member = None):
        """Set the user as captain of a team"""
        try:
            member = member or ctx.author
            self.join_as_master(ctx.message.author.guild, ctx.message.channel, member)
            await ctx.send(_('join_game_as_master', user=member.name))
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
                await ctx.send(_('word_guessed', word=word))
            else:
                await ctx.send(_('word_not_guessed', word=word))
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

    @commands.command()
    async def changeteam(self, ctx, *, member: discord.Member = None):
        try:
            member = member or ctx.author
            self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].change_team(member)
            await ctx.send(self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].print_members())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    """The commands for handle the start, join and stop of a game

        !start - start a game in which player can join with join command.

        !join - Join in the game. Allowed only if the game is JOINABLE

        !leave - leave the game. Allowed only if the game is JOINABLE

        !play - The game start and is not joinable anymore

        !stop - Stop the game

        !status - Send the status
       """

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
            self.game_helper.start(ctx.message.author.guild, ctx.message.channel)
            member = member or ctx.author
            await ctx.send(_('start_game', user=member.name))
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def join(self, ctx, *, member: discord.Member = None):
        """ Join in the game. Allowed only if the game is JOINABLE

        """
        print(ctx.message)
        try:
            self.game_helper.join(ctx.message.guild.id, ctx.message.channel.id, ctx.author)
            member = member or ctx.author
            await ctx.send(_('join_game', user=member.name))
            await ctx.send(self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].print_members())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def leave(self, ctx, *, member: discord.Member = None):
        """leave the game. Allowed only if the game is JOINABLE

        """
        print(ctx.message)
        try:
            self.game_helper.leave(ctx.message.guild.id, ctx.message.channel.id, ctx.author)
            member = member or ctx.author
            await ctx.send(_('leave_game', user=member.name))
            await ctx.send(self.game_helper.matches[(ctx.message.author.guild.id, ctx.message.channel.id)].print_members())
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def play(self, ctx, tag, *, member: discord.Member = None):
        """ The game start and is not joinable anymore

        """
        print(ctx.message)
        try:
            self.game_helper.play(ctx.message.guild.id, ctx.message.channel.id, tag)
            member = member or ctx.author
            await ctx.send(_('play_game', user=member.name, tag=tag))
            await self.send_images(ctx)
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def stop(self, ctx, *, member: discord.Member = None):
        """ Stop the game

            """
        print(ctx.message)
        try:
            self.game_helper.stop(ctx.message.guild.id, ctx.message.channel.id)
            member = member or ctx.author
            await ctx.send(_('stop_game', user=member.name))
        except NotAllowedCommand as err:
            await ctx.send(err.message)

    @commands.command()
    async def status(self, ctx):
        """ send the status

        """
        print(ctx.message)
        await ctx.send(self.game_helper.print_status())
