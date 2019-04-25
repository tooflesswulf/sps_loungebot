from discord.ext import commands
import discord


class EmbedListPrinter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='p')
    async def test_print(self, ctx: commands.Context):
        e = discord.Embed(title='Emoji List')

        ids = [e.guild_id for e in ctx.bot.emojis]
        ids_order = sorted(set(ids))

        if ctx.guild.emojis:
            text = ''
            for m in ctx.guild.emojis:
                text += '{}\t`:{}:`\n'.format(str(m), m.name)
            e.add_field(name='Server ' + ctx.guild.name, value=text)

        for i in ids_order:
            if i == ctx.guild.id:
                continue

            g = ctx.bot.get_guild(i)

            text = ''
            for m in g.emojis:
                text += '{}\t`:{}:`\n'.format(str(m), m.name)
            e.add_field(name='Server ' + g.name, value=text)

        # text = ''
        # for moji in ctx.bot.emojis:
        #     text += '{}\t`:{}:`\n'.format(str(moji), moji.name)

        # await ctx.message.channel.send(text)
        # e = discord.Embed(color=0x50bdfe)
        # e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
