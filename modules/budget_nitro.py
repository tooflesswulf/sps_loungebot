from discord.ext import commands


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
        text = ' '.join(text)
        await ctx.send(sender + text)
        await ctx.message.delete()

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
