from discord.ext import commands

import re
import numpy as np


class BudgetNitro(commands.Cog):
    description = 'This cog exists to satisfy peoples desire for animated emojis. Vvv important.'

    def __init__(self, bot):
        self.bot = bot

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
            outstr = ''
            for moji in ctx.bot.emojis:
                outstr += '{}\t`:{}:`\n'.format(str(moji), moji.name)
            await ctx.message.channel.send(outstr)
            return

        sender = '{} says:\n'.format(ctx.author.mention)
        text = await self.convert_emojis(ctx, ' '.join(text))
        await ctx.send(sender + text)
        await ctx.message.delete()

    async def convert_emojis(self, ctx, text):
        splits = EmojiSplitter(text).splits
        converter = commands.EmojiConverter()

        stringbuilder = ''

        for valid, string in splits:
            if not valid:
                stringbuilder += string
                continue

            ixs = np.array([i for i, v in enumerate(string) if v == ':'])

            i = 0
            while i + 1 < len(ixs):
                substr = string[ixs[i] + 1:ixs[i + 1]]
                try:
                    emoji_obj = await converter.convert(ctx, substr)
                except commands.BadArgument:
                    i += 1
                    continue

                stringbuilder += string[0:ixs[i]]
                stringbuilder += str(emoji_obj)
                string = string[ixs[i + 1] + 1:]
                ixs -= ixs[i + 1] + 1
                i += 2
            stringbuilder += string

        return stringbuilder

    # async def check_emoji(self, ):

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
