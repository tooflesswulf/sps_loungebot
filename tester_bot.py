import discord
from discord.ext import commands
import asyncio

from modules import MyDiscordClient as mdc

import module_loader

cmd_prefix = ';'
client = mdc.MyBot(cmd_prefix, description='Happy test bot. If u dont see awoo saying this tell Ablert to fix this shit')

module_loader.load_modules(client)


@client.command()
async def ping(ctx):
    await ctx.send('ping')


@client.event
async def on_ready():
    print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
    print('------------')


client.run('NTIwMzIwMzQzMDQzMjExMjg1.XK1XzA.95zdEiAjehH8cjMOV0nXz91TR4I')
