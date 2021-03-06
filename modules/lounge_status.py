from discord.ext import commands

import discord
import asyncio
import pickle
import socket, time, traceback, threading
import datetime as dt

status_msgs = [
    'door is closed',
    'door is open',
    'pi is offline',
    'Fatal error. Plz keep error log.'
]


class LoungeDoorStatus(commands.Cog):
    description = 'This cog exists to notify people about the state of the lounge'

    cur_status = 2
    keep_alive = True
    status_setter_lock = False
    server_address = ('169.254.72.29', 8789)
    update_freq = 3  # s

    '''
    Initializes this bot with the subscribers list and status-grabbing thread.
    '''

    def __init__(self, bot):
        self.bot = bot
        self.notif_file = 'subscribed_ids.pkl'
        try:
            with open(self.notif_file, 'rb') as f:
                self.notif_people = pickle.load(f)
        except (OSError, IOError) as e:
            self.notif_people = []
            with open(self.notif_file, 'wb') as f:
                pickle.dump(self.notif_people, f)

        self.status_thread = threading.Thread(target=self.status_getter)

    @commands.command(name='lounge',
                      brief='Replies with the current status of the lounge door',
                      description='Replies with the current status of the lounge door')
    async def status_resp(self, ctx: commands.Context):
        await ctx.channel.send(status_msgs[self.cur_status])

    @commands.command(name='sub',
                      brief='Sends you a DM when the door opens or closes',
                      description='Sends you a DM when the door opens or closes')
    async def subscribe_handler(self, ctx: commands.Context):
        if ctx.message.author.id in self.notif_people:
            await ctx.author.send('You\'re already subscribed. {}unsub to unsubscribe.'
                                  .format(ctx.bot.command_prefix))
            return
        self.notif_people.append(ctx.author.id)
        with open(self.notif_file, 'wb') as f:
            pickle.dump(self.notif_people, f)
        await ctx.author.send('Subscribed you to door state change updates. ' +
                              '{}unsub to unsubscribe.'.format(ctx.bot.command_prefix))

    @commands.command(name='unsub',
                      brief='Stops sending you DM\'s',
                      description='Stops sending you DM\'s')
    async def unsubscribe_handler(self, ctx: commands.Context):
        try:
            self.notif_people.remove(ctx.author.id)
        except ValueError:
            await ctx.author.send('You\'re not subscribed.')
            return
        with open(self.notif_file, 'wb') as f:
            pickle.dump(self.notif_people, f)
        await ctx.author.send('You\'re now unsubscribed.')

    # Threaded function for getting the door state from the pi.
    def status_getter(self):
        while self.keep_alive:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                sock.connect(self.server_address)
                print('Opened socket')
            except (ConnectionRefusedError, socket.gaierror) as e:
                print('Socket could not be opened. Trying again.')
                continue

            status = LazyStateChange()
            status.state = self.cur_status
            while self.keep_alive:
                try:
                    sock.send(b'1')
                    ret = sock.recv(1)
                    if ret == b'1':
                        status.suggest(1)
                    else:
                        status.suggest(0)

                    self.cur_status = status.state
                    time.sleep(.05)
                except (ConnectionResetError, IOError) as e:
                    self.cur_status = 2
                    status.state = 2
                    print('got connection/io error:')
                    print(e)
                    print('\nTrying to restart anyways.')
                    time.sleep(1)
                    break
                except Exception as e:
                    self.cur_status = 3
                    status.state = 3
                    sock.close()
                    print('some other error:')
                    print(traceback.format_exc())
                    with open('error_{}.txt'.format(time.time())) as f:
                        f.write(traceback.format_exc())
                    return

            sock.close()
            print('closed socket')

    # Starts the pi listener, blocking until its connected.
    def start_pi_listener(self):
        print('Waiting for socket to exist')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_address)
        sock.close()

        # Starts the getter thread
        self.status_thread.start()

    async def change_status(self, txt):
        await self.bot.change_presence(activity=discord.Game(name=txt))

        t = dt.datetime.now()
        timestr = '`EDT {:d}:{:02d}`\t'.format(t.hour, t.minute)

        for uid in self.notif_people:
            await self.bot.get_user(uid).send(timestr + txt)

    @commands.Cog.listener(name='on_ready')
    async def status_setter(self):
        if self.status_setter_lock:
            return

        cur_set = self.cur_status
        self.status_setter_lock = True
        print('Starting status setter')
        await self.bot.change_presence(activity=discord.Game(name=status_msgs[cur_set]))

        while self.keep_alive:
            if cur_set != self.cur_status:
                cur_set = self.cur_status
                await self.change_status(status_msgs[cur_set])
                await asyncio.sleep(self.update_freq)
                continue
            await asyncio.sleep(.05)

        print('Unloaded status setter')
        self.status_setter_lock = False

    def cog_unload(self):
        self.keep_alive = False
        self.status_thread.join()


# Requires 5 of the same signal in a row to change the state. Truly lazy.
class LazyStateChange:
    state = 2
    next = -1
    cnt = 0

    def suggest(self, n):
        if self.next == n:
            self.cnt += 1
            if self.cnt >= 5:
                self.state = n
                self.cnt = 0
            return

        self.next = n
        self.cnt = 0
