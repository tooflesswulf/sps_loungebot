from discord.ext import commands
import discord

import re
import numpy as np


class BudgetNitro(commands.Cog):
    description = 'This cog exists to satisfy peoples desire for animated emojis. Vvv important.'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='nl',
        brief='Lists all custom emojis this bot has access to',
        description='Lists all custom emojis this bot has access to',
    )
    async def emoji_list(self, ctx):
        outstr = ''
        for moji in ctx.bot.emojis:
            outstr += '{}\t`:{}:`\n'.format(str(moji), moji.name)
        await ctx.message.channel.send(outstr)

    @commands.command(
        name='nitro',
        brief='Converts emojis tags in your message to make you feel rich',
        description='Prints your text back out at you. Emoji codes will be '
                    'converted to emojis, including animated ones and ones from '
                    'other servers (hence the nitro).\n'
                    'Type nitro list to list all available emojis.'
    )
    async def emoji_converter(self, ctx, *text):
        if len(text) == 0:
            await ctx.send('You gotta put something fam.')
            return

        if len(text) == 1 and text[0] in ['list', 'l']:
            await self.emoji_list.invoke(ctx)
            return

        text = await convert_emojis(ctx, ' '.join(text))
        e = discord.Embed(description=text)
        e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

        if isinstance(ctx.channel, discord.DMChannel) or isinstance(ctx.channel, discord.GroupChannel):
            return
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

    # shh secret functions
    @commands.Cog.listener('on_message')
    async def call_albert(self, msg):
        if not msg.content.lower().startswith(self.bot.command_prefix + 'albert'):
            return

        try:
            name = msg.channel.name
            guild = msg.channel.guild
        except AttributeError:
            await self.bot.get_user(97477826969616384).send('U got poked by {} in DM'.format(msg.author.name))
            return

        await self.bot.get_user(97477826969616384).send(
            'U got poked in {}#{}'.format(guild, name))


class EmojiSplitter():
    def __init__(self, text):
        self.text = text
        self.splits = []
        m = re.search(r'<a?:[a-zA-Z0-9_]+:[0-9]+>', text)
        while m:
            self.push_str(text[0:m.start(0)])
            self.push_em(text[m.start(0):m.end(0)])
            text = text[m.end(0):]
            m = re.search(r'<a?:[a-zA-Z0-9_]+:[0-9]+>', text)
        self.push_str(text)

    def push_str(self, str):
        self.splits.append((True, str))

    def push_em(self, str):
        self.splits.append((False, str))


async def convert_emojis(ctx, text):
    splits = EmojiSplitter(text).splits

    ret_str = ''

    for valid, string in splits:
        if not valid:
            ret_str += string
            continue

        ixs = np.array([i for i, v in enumerate(string) if v == ':'])

        i = 0
        while i + 1 < len(ixs):
            substr = string[ixs[i] + 1:ixs[i + 1]]

            emoji_obj = discord.utils.get(ctx.guild.emojis, name=substr)
            if emoji_obj is None:
                emoji_obj = discord.utils.get(ctx.bot.emojis, name=substr)

            if emoji_obj is None:
                i += 1
                continue

            ret_str += string[0:ixs[i]]
            ret_str += str(emoji_obj)
            string = string[ixs[i + 1] + 1:]
            ixs -= ixs[i + 1] + 1
            i += 2
        ret_str += string

    return ret_str
