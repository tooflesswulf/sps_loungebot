import discord
from modules import MyDiscordClient as mdc

from modules import budget_nitro


def load_modules(client, debug=False):
    for z in budget_nitro.module_commands():
        for k in z[0]:
            client.command(name=k)(z[1])

    pass
