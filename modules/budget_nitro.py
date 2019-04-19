async def emoji_converter(ctx, *text):
    if len(text) == 0:
        await ctx.send('You gotta put something fam.')
        return

    sender = '{} says:\n'.format(ctx.author.mention)
    text = ' '.join(text)
    await ctx.send(sender + text)
    await ctx.message.delete()


def module_commands():
    return (['nitro', 'em'], emoji_converter)

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
