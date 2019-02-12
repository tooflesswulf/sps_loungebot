import socket
import discord
import asyncio
import time
import traceback
import pickle
import logging

control_char = '!'

retry_period = 60  # s
update_freq = 3  # s
timemacro = lambda: time.strftime('%m-%d GMT %H:%M', time.gmtime())

status_msgs = [
    'door is closed',
    'door is open',
    'pi is offline'
]
cur_status = 2
log_file = 'loungebot.log'
notif_file = 'subscribed_ids.pkl'
try:
    with open(notif_file, 'rb') as f:
        notif_people = pickle.load(f)
except (OSError, IOError) as e:
    notif_people = []
    with open(notif_file, 'wb') as f:
        pickle.dump(notif_people, f)

client = discord.Client()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def print_log(msg):
    print('[{}] '.format(timemacro()) + msg)
    with open(log_file, 'a') as f:
        f.write('[{}] [{}] {}\n'.format(timemacro(), time.time(), msg))


async def change_status(msg):
    await client.change_presence(game=discord.Game(name=msg))

    # notify all subscribers
    for uid in notif_people:
        user = await client.get_user_info(uid)
        await client.send_message(user, msg)


async def read_pi():
    global cur_status
    # server_address = ('raspberrypi.local', 8789)
    server_address = ('169.254.72.29', 8789)
    await client.change_presence(game=discord.Game(name=status_msgs[cur_status]))

    while True:
        try:
            reader, writer = await asyncio.open_connection(*server_address)
        except (ConnectionRefusedError, socket.gaierror):
            print('Could not connect to pi. Waiting %d sec to try again' % retry_period)
            await asyncio.sleep(retry_period)
            continue
        except Exception as e:
            print(e)
            break

        try:
            while True:
                writer.write(b'1')
                data = await reader.read(1)
                prev_status = cur_status
                if data == b'1':
                    cur_status = 1
                else:
                    cur_status = 0
                if prev_status != cur_status:
                    print_log('Door state changed to {}'.format(cur_status))
                    # await client.change_presence(game=discord.Game(name=status_msgs[cur_status]))
                    await change_status(status_msgs[cur_status])
                await asyncio.sleep(update_freq)
        except (ConnectionResetError, IOError):
            print_log('Pi went offline.')
            cur_status = 2
            # await client.change_presence(game=discord.Game(name=status_msgs[cur_status]))
            await change_status(status_msgs[cur_status])
            continue
        except Exception as e:
            print_log('Something went wrong. stopping.')
            print_log(traceback.format_exc())
            break
        finally:
            writer.close()
            await writer.wait_closed()


@client.event
async def on_ready():
    print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
    print('------------')

    client.loop.create_task(read_pi())


@client.event
async def on_message(message):
    if message.content.startswith(control_char):
        msg = message.content[1:]
        if msg in ['lounge']:
            await client.send_message(message.channel, status_msgs[cur_status])
            return
        elif msg in ['subscribe', 'sub']:
            if message.author.id in notif_people:
                await client.send_message(message.author,
                                          'You\'re already subscribed. {}unsub to unsubscribe.'.format(control_char))
                return
            notif_people.append(message.author.id)
            with open(notif_file, 'wb') as f:
                pickle.dump(notif_people, f)
            await client.send_message(message.author,
                                      'Subscribed you to door state change updates. ' +
                                      '{}unsub to unsubscribe.'.format(control_char) +
                                      '\nWARNING: can be very spammy')
            print_log('Subscribed user {}({})'.format(message.author.id, message.author.name))
            return
        elif msg in ['unsubscribe', 'usub', 'unsub']:
            if message.author.id not in notif_people:
                await client.send_message(message.author,
                                          'You\'re not subscribed.'.format(control_char))
                return

            notif_people.remove(message.author.id)
            with open(notif_file, 'wb') as f:
                pickle.dump(notif_people, f)
            await client.send_message(message.author, 'You\'re now unsubscribed.')
            print_log('Unsubscribed user {}({})'.format(message.author.id, message.author.name))
            return


client.run('NTE1NDIyNzk1NDIxOTc0NTY5.Dtk5fw.7Zn7_C2jacI4oNos2xbeEYDheFo')
