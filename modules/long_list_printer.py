from discord.ext import commands
import discord


class EmbedListPrinter(commands.Cog):
    fields = []
    title = None
    msg = None
    has_pages = False

    def __init__(self, ctx, max_len=50):
        self.bot = ctx.bot
        self.author = ctx.author
        self.max_len = max_len

    def add_field(self, name='', value=''):
        v_len = value.count('\n')
        self.fields.append((name, value, v_len))

    async def send(self, ctx):
        e = discord.Embed(title=self.title)
        for n, v, l in self.fields:
            e.add_field(name=n, value=v)
        self.msg = await ctx.send(embed=e)

    @commands.Cog.listener(name='on_reaction_add')
    async def change_page(self, ctx):
        if not self.has_pages or ctx.author != self.author:
            return
        await ctx.send('Please wait, feature coming soon!')

    # @commands.command(name='p')
    # async def test_print(self, ctx: commands.Context):
    #     e = discord.Embed(title='Emoji List')
    #
    #     ids = [e.guild_id for e in ctx.bot.emojis]
    #     ids_order = sorted(set(ids))
    #
    #     if ctx.guild.emojis:
    #         text = ''
    #         for m in ctx.guild.emojis:
    #             text += '{}\t`:{}:`\n'.format(str(m), m.name)
    #         e.add_field(name='Server ' + ctx.guild.name, value=text)
    #
    #     for i in ids_order:
    #         if i == ctx.guild.id:
    #             continue
    #
    #         g = ctx.bot.get_guild(i)
    #
    #         text = ''
    #         for m in g.emojis:
    #             text += '{}\t`:{}:\t|\t{}`\n'.format(str(m), m.name, m.id)
    #         e.add_field(name='Server ' + g.name, value=text, inline=False)
    #
    #     # text = ''
    #     # for moji in ctx.bot.emojis:
    #     #     text += '{}\t`:{}:`\n'.format(str(moji), moji.name)
    #
    #     # await ctx.message.channel.send(text)
    #     # e = discord.Embed(color=0x50bdfe)
    #     # e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=e)
