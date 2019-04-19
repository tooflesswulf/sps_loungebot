import discord
import asyncio
import pickle
import socket, time, traceback, threading
from modules import MyDiscordClient as mdc

update_freq = 3  # s

status_msgs = [
    'door is closed',
    'door is open',
    'pi is offline'
]

notif_file = 'subscribed_ids.pkl'
try:
    with open(notif_file, 'rb') as f:
        notif_people = pickle.load(f)
except (OSError, IOError) as e:
    notif_people = []
    with open(notif_file, 'wb') as f:
        pickle.dump(notif_people, f)


def module_commands(client: mdc.Client):
    cc = client.command_prefix

    status_resp_desc = 'Responds with the current state of the lounge door.'

    async def status_resp(msg):
        await msg.channel.send(status_msgs[client.cur_status])

    subscribe_handler_desc = 'Sends you a DM whenever the door is opened or closed.'

    async def subscribe_handler(msg):
        if msg.author.id in notif_people:
            await msg.author.send('You\'re already subscribed. {}unsub to unsubscribe.'.format(cc))
            return
        notif_people.append(msg.author.id)
        with open(notif_file, 'wb') as f:
            pickle.dump(notif_people, f)
        await msg.author.send('Subscribed you to door state change updates. ' +
                              '{}unsub to unsubscribe.'.format(cc))
        print('Subscribed user {}({})'.format(msg.author.id, msg.author.name))
        return

    unsub_handler_desc = 'Undoes the subscribe command above.'

    async def unsub_handler(msg):
        if msg.author.id not in notif_people:
            await msg.author('You\'re not subscribed.'.format(cc))
            return

        notif_people.remove(msg.author.id)
        with open(notif_file, 'wb') as f:
            pickle.dump(notif_people, f)
        await msg.author.send('You\'re now unsubscribed.')
        print('Unsubscribed user {}({})'.format(msg.author.id, msg.author.name))
        return

    return [
        (['r', 'lounge'], status_resp, status_resp_desc),
        (['subscribe', 'sub'], subscribe_handler, subscribe_handler_desc),
        (['unsubscribe', 'usub', 'unsub'], unsub_handler, unsub_handler_desc),
    ]


def load_tasks(client: mdc.Client):
    async def change_status(txt):
        await client.change_presence(activity=discord.Game(name=txt))

        # notify all subscribers
        for uid in notif_people:
            user = client.get_user(uid)
            await user.send(txt)

    async def status_setter():
        cur_set = client.cur_status
        await client.change_presence(activity=discord.Game(name=status_msgs[cur_set]))

        while True:
            try:
                if cur_set != cur_status:
                    client.cur_status = cur_status
            except NameError:
                pass

            if cur_set != client.cur_status:
                cur_set = client.cur_status
                await change_status(status_msgs[cur_set])
            await asyncio.sleep(update_freq)

    return [status_setter]


# Code for single-thread pi zero communication program.
# Exposes the read status as a global variable
def create_pi_communicator():
    keep_alive = True
    server_address = ('169.254.72.29', 8789)

    def status_getter():
        global cur_status
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect(server_address)
        print('Opened socket')
        while keep_alive:
            try:
                sock.send(b'1')
                ret = sock.recv(1)
                if ret == b'1':
                    cur_status = 1
                else:
                    cur_status = 0

                time.sleep(update_freq / 2)
            except (ConnectionResetError, IOError) as e:
                cur_status = 2
                print('got connection/io error:')
                print(e)
                break
            except Exception as e:
                print('some other error:')
                print(traceback.format_exc())
                break

        sock.close()
        print('closed socket')

    print('Waiting for socket to exist')
    socksboi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socksboi.connect(server_address)
    socksboi.close()

    t = threading.Thread(target=status_getter)
    t.start()

    return t
