import discord
from discord.ext import commands
import asyncio

import module_loader

cmd_prefix = ';'
client = commands.Bot(cmd_prefix,
                      description='Happy test bot. Awooooo...\n'
                                  'tell Albert to fix this shit')

module_loader.load_modules(client, debug=True)


@client.event
async def on_ready():
    print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
    print('------------')


client.run('NTIwMzIwMzQzMDQzMjExMjg1.XK1XzA.95zdEiAjehH8cjMOV0nXz91TR4I')
print('Properly exited')
