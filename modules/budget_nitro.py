import discord
import asyncio
from modules import MyDiscordClient as mdc

import discord.ext.commands as cmds

cmds.EmojiConverter()


def module_commands(client: mdc.Client):
    async def paste_msg(msg):
        args = msg.content.split()
        if len(args) == 1:
            await msg.channel.send('You gotta put something fam.')
            return
        if len(args) == 2 and args[1] in ['help', 'h']:
            outstr = ''
            for moji in client.emojis:
                outstr += '{}\t`:{}:`\n'.format(str(moji), moji.name)
            await msg.channel.send(outstr)
            return

        sender = '{} says:\n'.format(msg.author.mention)
        text = replace_emoji(' '.join(args[1:]), client.emojis)
        await msg.channel.send(sender + text)
        print('log:\n' + text)
        await msg.delete()

    return [
        (['nitro', 'em'], paste_msg, 'Deletes you message and pastes your message verbatim. '
                                     'Used for poor people to simulate Nitro i guess.')
    ]


def replace_emoji(text, emojis):
    ixs = [i for i, v in enumerate(text) if v == ':']
    newtext = ''
    end_ix = 0

    i = 0
    while i + 1 < len(ixs):
        substr = text[ixs[i] + 1:ixs[i + 1]]
        e = conv_emoji(substr)
        print('hello there\n'+str(e))
        # for e in emojis:
        #     if e.name == substr:
        #         newtext += text[end_ix : ixs[i]] + str(e)
        #         end_ix = ixs[i+1] + 1
        #         i+=1
        #         break
        i += 1

    try:
        return newtext + text[end_ix:]
    except IndexError:
        return newtext


def conv_emoji(arg: discord.Emoji):
    return arg
