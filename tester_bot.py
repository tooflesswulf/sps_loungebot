import socket
import discord
import asyncio
import time
import traceback
import pickle
import threading

import module_loader

client = module_loader.client
client.control_char = ';'

commands = module_loader.load_commands()
tasks = module_loader.load_tasks()

reboot_freq = 86400


@client.event
async def on_ready():
    print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
    print('------------')

    for t in tasks:
        client.loop.create_task(t())


@client.event
async def on_message(message):
    if message.content.startswith(client.control_char):
        cmd = message.content[len(client.control_char):].split()[0]
        for k, f in commands:
            if cmd in k:
                print('Executing function with message {}'.format(cmd))
                await f(message)


async def kill_task():
    await asyncio.sleep(reboot_freq)
    raise SystemExit


tasks += [kill_task]


def handle_exit():
    print("Handling client exit")
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass


while True:
    client.event(on_ready)
    client.event(on_message)

    try:
        client.loop.run_until_complete(client.start('NTIwMzIwMzQzMDQzMjExMjg1.XK1XzA.95zdEiAjehH8cjMOV0nXz91TR4I'))
    except (KeyboardInterrupt, RuntimeError):
        break
    except SystemExit:
        handle_exit()

    print("Bot restarting")
    client = discord.Client(loop=client.loop)

keep_alive = False
handle_exit()
# t.join()
print('Program exited properly')
