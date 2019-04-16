import discord
import asyncio


def module_commands(client):
    async def paste_msg(msg):
        args = msg.content.split()
        if len(args) == 1:
            await client.send_message(msg.channel, 'You gotta put something fam.')
            return
        text = ' '.join(args[1:])
        print(text)
        # moji = discord.utils.get(client.get_all_emojis(), name=text)
        moji = client.emojis[0]
        await client.send_message(msg.channel, str(moji))

    return [
        (['nitro', 'em'], paste_msg, 'Deletes you message and pastes your message verbatim. '
                                     'Used for poor people to simulate Nitro I guess.')
    ]
