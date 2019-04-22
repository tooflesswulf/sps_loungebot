from discord.ext import commands

import module_loader

cmd_prefix = '!'
client = commands.Bot(cmd_prefix,
                      description='Discord bot primarily made to broadcast '
                                  'the status of the lounge. Other features have been added because.')

module_loader.load_modules(client, use_raspi=True)


@client.event
async def on_ready():
    print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
    print('------------')


client.run('NTE1NDIyNzk1NDIxOTc0NTY5.XLuL1A.q-wF5D987vpYlOq4kvuyCLsgX0U')
print('Properly exited')
