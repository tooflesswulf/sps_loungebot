import discord
import asyncio

import module_loader

cmd_prefix = ';'
reboot_freq = 86400
# reboot_freq = 8

client = module_loader.setup_client(cmd_prefix, debug=True)


async def kill_task():
    while True:
        await asyncio.sleep(reboot_freq)
        raise SystemExit


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


if __name__ == '__main__':
    client.loop.create_task(kill_task())
    while True:
        try:
            client.loop.run_until_complete(client.start('NTIwMzIwMzQzMDQzMjExMjg1.XK1XzA.95zdEiAjehH8cjMOV0nXz91TR4I'))
        except (KeyboardInterrupt, RuntimeError):
            break
        except SystemExit:
            handle_exit()

        print("Bot restarting")
        client = client.freshcopy()
        client = module_loader.setup_client(cmd_prefix, old_client=client, debug=True)
        client.loop.create_task(kill_task())
    # try:
    #     client.loop.run_until_complete(client.start('NTIwMzIwMzQzMDQzMjExMjg1.XK1XzA.95zdEiAjehH8cjMOV0nXz91TR4I'))
    # except KeyboardInterrupt:
    #     pass

    handle_exit()
    print('Program exited properly')
