import discord
import asyncio
from modules import MyDiscordClient as mdc


def module_commands(client: mdc.Client):
    change_cur_status_desc = 'Sets `client.cur_status` to the next number. Used for debug only.'

    async def change_cur_status(msg):
        args = msg.content.split()
        try:
            nxt = int(args[1])
            if 0 > nxt or nxt > 2:
                raise ValueError
        except (IndexError, ValueError):
            msg.channel.send('Need valid status number (0-2 int)')
            return

        client.cur_status = nxt

    return [
        (['cs'], change_cur_status, change_cur_status_desc)
    ]
