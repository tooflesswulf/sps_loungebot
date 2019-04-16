import discord

from modules import lounge_status, test_functions, budget_nitro

client = discord.Client()


def load_commands():
    cmd = test_functions.module_commands(client)
    cmd += lounge_status.module_commands(client)
    cmd += budget_nitro.module_commands(client)

    return conv_help(cmd)


def load_tasks():
    tasks = lounge_status.load_tasks(client)

    return tasks


def conv_help(cmd):
    help_key = ['h', 'help']
    cmd.append((help_key, None, 'Prints the help menu.'))

    newcmds = []
    helpstring = '```'

    cc = client.control_char
    for key, func, desc in cmd:
        helpstring += cc + (', ' + cc).join(key) + '\n\t' + desc + '\n\n'
        newcmds.append((key, func))

    helpstring += '```'

    async def printhelp(msg):
        await client.send_message(msg.channel, helpstring)

    newcmds[-1] = ((help_key, printhelp))
    return newcmds
