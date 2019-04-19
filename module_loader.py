import discord
from modules import MyDiscordClient as mdc

from modules import lounge_status, test_functions, budget_nitro


def load_commands():
    cmd = test_functions.module_commands(client)
    cmd += lounge_status.module_commands(client)
    cmd += budget_nitro.module_commands(client)

    return conv_help(cmd)


def load_tasks():
    tasks = lounge_status.load_tasks(client)

    return tasks


def setup_client(cmd_prefix, loop=None):
    global client

    try:
        client = client.freshcopy(loop)
    except NameError:
        print('This should be first time starting.')
        client = mdc.Client()

    client.command_prefix = cmd_prefix

    commands = load_commands()
    tasks = load_tasks()

    @client.event
    async def on_message(message):
        if message.content.startswith(client.command_prefix):
            cmd = message.content[len(client.command_prefix):].split()[0]
            for k, f in commands:
                if cmd in k:
                    await f(message)

    @client.event
    async def on_ready():
        print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
        print('------------')

        for t in tasks:
            client.loop.create_task(t())

    return client


def conv_help(cmd):
    help_key = ['h', 'help']
    cmd.append((help_key, None, 'Prints the help menu.'))

    newcmds = []
    helpstring = '```'

    cc = client.command_prefix
    for key, func, desc in cmd:
        helpstring += cc + (', ' + cc).join(key) + '\n\t' + desc + '\n\n'
        newcmds.append((key, func))

    helpstring += '```'

    async def printhelp(msg):
        await msg.channel.send(helpstring)

    newcmds[-1] = ((help_key, printhelp))
    return newcmds
