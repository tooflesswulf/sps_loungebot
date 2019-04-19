from discord.ext import commands


class BudgetNitro(commands.Cog):
    @commands.command(
        name='nitro',
        brief='Converts emojis tags in your message to make you feel rich',
        description='Prints your text back out at you. Emoji codes will be ' +
                    'converted to emojis, including animated ones and ones from ' +
                    'other servers (hence the nitro).\n'
                    'Type nitro list to list all available emojis.'
    )
    async def emoji_converter(self, ctx, *text):
        if len(text) == 0:
            await ctx.send('You gotta put something fam.')
            return

        if len(text) == 1 and text[0] in ['help', 'h']:
            outstr = ''
            for moji in ctx.bot.emojis:
                outstr += '{}\t`:{}:`\n'.format(str(moji), moji.name)
            await ctx.message.channel.send(outstr)
            return

        sender = '{} says:\n'.format(ctx.author.mention)
        text = ' '.join(text)
        await ctx.send(sender + text)
        await ctx.message.delete()

    # args = msg.content.split()
    # if len(args) == 1:
    #     await msg.channel.send('You gotta put something fam.')
    #     return
    # if len(args) == 2 and args[1] in ['help', 'h']:
    #     outstr = ''
    #     for moji in client.emojis:
    #         outstr += '{}\t`:{}:`\n'.format(str(moji), moji.name)
    #     await msg.channel.send(outstr)
    #     return
    #
    # sender = '{} says:\n'.format(msg.author.mention)
    # # text = replace_emoji(' '.join(args[1:]), client.emojis)
    # await msg.channel.send(sender + text)
    # print('log:\n' + text)
    # await msg.delete()

    # return [
    #     (['nitro', 'em'], paste_msg, 'Deletes you message and pastes your message verbatim. '
    #                                  'Used for poor people to simulate Nitro i guess.')
    # ]
