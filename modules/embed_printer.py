from discord.ext import commands
import discord

import time
from time import strftime


class EmbedPrinter(commands.Cog):
    def __init__(self, bot, n):
        self.bot = bot
        self.id = n

    @commands.command(name='p')
    async def test_print(self, ctx, n, *text):
        if n != self.id:
            return
        if len(text) == 0:
            await ctx.send('Input something plz!')
            return
        text = ' '.join(text)

        ct = strftime('Today at %I:%M %p', time.localtime())

        # e = discord.Embed(color=0x50bdfe)
        e = discord.Embed(description=text)
        e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        e.set_footer(text='From printer {}'.format(self.id))
        await ctx.send(embed=e)
