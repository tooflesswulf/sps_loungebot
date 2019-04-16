import discord
import asyncio
import pickle

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


def module_commands(client):
    status_resp_desc = 'Responds with the current state of the lounge door.'

    async def status_resp(msg):
        await client.send_message(msg.channel, status_msgs[client.cur_status])

    subscribe_handler_desc = 'Sends you a DM whenever the door is opened or closed.'

    async def subscribe_handler(msg):
        if msg.author.id in notif_people:
            await client.send_message(msg.author,
                                      'You\'re already subscribed. {}unsub to unsubscribe.'.format(client.control_char))
            return
        notif_people.append(msg.author.id)
        with open(notif_file, 'wb') as f:
            pickle.dump(notif_people, f)
        await client.send_message(msg.author,
                                  'Subscribed you to door state change updates. ' +
                                  '{}unsub to unsubscribe.'.format(client.control_char))
        print('Subscribed user {}({})'.format(msg.author.id, msg.author.name))
        return

    unsub_handler_desc = 'Undoes the subscribe command above.'

    async def unsub_handler(msg):
        if msg.author.id not in notif_people:
            await client.send_message(msg.author,
                                      'You\'re not subscribed.'.format(client.control_char))
            return

        notif_people.remove(msg.author.id)
        with open(notif_file, 'wb') as f:
            pickle.dump(notif_people, f)
        await client.send_message(msg.author, 'You\'re now unsubscribed.')
        print('Unsubscribed user {}({})'.format(msg.author.id, msg.author.name))
        return

    return [
        (['r', 'lounge'], status_resp, status_resp_desc),
        (['subscribe', 'sub'], subscribe_handler, subscribe_handler_desc),
        (['unsubscribe', 'usub', 'unsub'], unsub_handler, unsub_handler_desc),
    ]


def load_tasks(client):
    client.cur_status = 2

    async def change_status(txt):
        await client.change_presence(game=discord.Game(name=txt))

        # notify all subscribers
        for uid in notif_people:
            user = await client.get_user_info(uid)
            await client.send_message(user, txt)

    async def status_setter():
        cur_set = client.cur_status
        # await client.change_presence(game=discord.Game(name=status_msgs[cur_set]))

        while True:
            if cur_set != client.cur_status:
                cur_set = client.cur_status
                await change_status(status_msgs[cur_set])
            await asyncio.sleep(update_freq)

    return [status_setter]
