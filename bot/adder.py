import discord
from util.exception import NotAllowedCommand
from game.match import Match, Status
from discord.ext import commands
from game.database import Database
from util.strings import get_string_bot as _


class Adder(commands.Cog):
    """The commands for handle the adding of words

       """
    def __init__(self,bot):
        self.bot = bot
        self.user_tag = dict()
        self.db = Database() # it's the right place? 

    @commands.command()
    async def addtag(self, ctx, tag, lang, *, member: discord.Member = None):
        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.send(_('error_addtag_private'))
        else:
            try:
                member = member or ctx.author
                self.db.add_tag(tag, lang)
                await ctx.send(_('tag_added', tag = tag))
            except NotAllowedCommand as err:
                await ctx.send(err.message)

    @commands.command()
    async def addword(self, ctx, tag, *, member: discord.Member = None):

        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.send(_('error_addword_private'))
        else:
            try:
                member = member or ctx.author
                if self.db.get_tag_id(tag) is not None:
                    self.user_tag[member.id] = tag
                    await ctx.send(_('tag_adding', tag = tag))
                else:
                    raise NotAllowedCommand(_('error_tag_not_exists', tag = tag))
            except NotAllowedCommand as err:
                await ctx.send(err.message)

    @commands.Cog.listener('on_message')
    async def word_listener(self, ctx, *, member: discord.Member = None):

        if ctx.author == self.bot.user:
            return
        member = member or ctx.author
        if isinstance(ctx.channel, discord.DMChannel) and member.id in self.user_tag.keys() and ctx.content[0] != '!':
            words = ctx.content.split('\n')
            #for each word in words, upperize the first letter
            words = [(lambda x: x[0].upper() + x[1:])(w) for w in words]
            self.db.add_words(words, self.user_tag[member.id])
            await ctx.send(_('words_added'))

    @commands.command()
    async def stopword(self, ctx, *, member: discord.Member = None):

        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.send(_('error_stopword_private'))
        else:
            try:
                member = member or ctx.author
                self.user_tag.pop(member.id, None)
                await ctx.send(_('stop_word'))
            except NotAllowedCommand as err:
                await ctx.send(err.message)

    @commands.command()
    async def listtags(self, ctx, *, member: discord.Member = None):
        try:
            member = member or ctx.author
            tags = self.db.get_tags()
            if len(tags) == 0:
                s = _('tags_empty')
            else:
                s = _('tags_available') + '\n'
                for (tag, lang) in tags:
                    s+='{} ({})\n'.format(tag,lang)
            await ctx.send(s)
        except NotAllowedCommand as err:
            await ctx.send(err.message)