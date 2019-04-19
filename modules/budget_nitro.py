import discord
import asyncio
from modules import MyDiscordClient as mdc


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
            await msg.author.send(outstr)
            return
        text = ' '.join(args[1:])
        moji = client.emojis[0]
        await msg.channel.send(str(moji))

    return [
        (['nitro', 'em'], paste_msg, 'Deletes you message and pastes your message verbatim. '
                                     'Used for poor people to simulate Nitro i guess.')
    ]
