from discord.ext import commands
from modules import budget_nitro, long_list_printer, test_functions, long_list_printer

cmd_prefix = ';'
client = commands.Bot(cmd_prefix,
                      description='REEEEE\n'
                                  'Tell Albert if u see this. Say bot is brooken and dumb')

client.add_cog(budget_nitro.BudgetNitro(client))
# client.add_cog(long_list_printer.EmbedListPrinter(client))
client.add_cog(test_functions.StatusTester(client))


@client.event
async def on_ready():
    print('Logged in as:\n\t{}\n\t{}'.format(client.user.name, client.user.id))
    print('------------')


client.run('NTIwMzIwMzQzMDQzMjExMjg1.XK1XzA.95zdEiAjehH8cjMOV0nXz91TR4I')
print('Properly exited')
