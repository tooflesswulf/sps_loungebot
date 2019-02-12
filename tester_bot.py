import discord
import logging
import pickle

control_char = ','

client = discord.Client()

notif_file = 'subscribed_ids.pkl'
with open(notif_file, 'rb') as f:
    notif_people = pickle.load(f)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@client.event
async def on_ready():
    print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
    print('------------')

    print(notif_people)


@client.event
async def on_message(message : discord.Message):
    if message.content.startswith(control_char):
        msg = message.content[1:]
        if msg in ['subscribe', 'sub']:
            if message.author.id in notif_people:
                await client.send_message(message.author,
                                          'You\'re already subscribed. {}unsub to unsubscribe.'.format(control_char))
                return
            notif_people.append(message.author.id)
            with open(notif_file, 'wb') as f:
                pickle.dump(notif_people, f)
            await client.send_message(message.author,
                                      'Subscribed you to door state change updates. {}unsub to unsubscribe.' +
                                      '\nWARNING: can be very spammy'.format(control_char))
            print('Subscribed user {}({})'.format(message.author.id, message.author.name))
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
            print('Unsubscribed user {}({})'.format(message.author.id, message.author.name))
            return


        elif msg in ['push']:
            for uid in notif_people:
                await client.send_message(await client.get_user_info(uid), 'pushed')



client.run('NTIwMzIwMzQzMDQzMjExMjg1.DusKHw.eNjRLg15gkiSqwBksp5FnCWgFV4')