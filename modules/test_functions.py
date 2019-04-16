import discord
import asyncio


def module_commands(client):
    change_cur_status_desc = 'Sets `client.cur_status` to the next number. Used for debug only.'

    async def change_cur_status(msg):
        args = msg.content.split()
        try:
            nxt = int(args[1])
            if 0 > nxt or nxt > 2:
                raise ValueError
        except (IndexError, ValueError):
            client.send_message(msg.channel, 'Need valid status number (0-2 int)')
            return

        client.cur_status = nxt

    return [
        (['cs'], change_cur_status, change_cur_status_desc)
    ]
