import discord
from modules import MyDiscordClient as mdc


def load_modules(client, debug=False):
    cmd = []
    if debug:
        from modules import test_functions
        cmd += test_functions.module_commands(client)

    from modules import lounge_status, budget_nitro
    cmd += lounge_status.module_commands(client)
    cmd += budget_nitro.module_commands(client)

    tasks = lounge_status.load_tasks(client)
    return conv_help(cmd, client.command_prefix), tasks


def setup_client(cmd_prefix, old_client=None, debug=False):
    if old_client:
        client = old_client.freshcopy()
    else:
        client = mdc.Client()
        print('This should be first time starting.')
        # Single-execution setup operations should be loaded here i guess
        if not debug:
            from modules import lounge_status
            lounge_status.create_pi_communicator()

    client.command_prefix = cmd_prefix

    commands, tasks = load_modules(client, debug=debug)

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


def conv_help(cmd, prefix):
    help_key = ['h', 'help']
    cmd.append((help_key, None, 'Prints the help menu.'))

    newcmds = []
    helpstring = '```'

    for key, func, desc in cmd:
        helpstring += prefix + (', ' + prefix).join(key) + '\n\t' + desc + '\n\n'
        newcmds.append((key, func))

    helpstring += '```'

    async def printhelp(msg):
        await msg.channel.send(helpstring)

    newcmds[-1] = ((help_key, printhelp))
    return newcmds
