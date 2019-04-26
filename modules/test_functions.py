from discord.ext import commands
from modules.long_list_printer import EmbedListPrinter


class StatusTester(commands.Cog):
    description = 'This cog is used for testing shit.\n' \
                  'IF YOU SEE THIS TELL ALBERT'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='cs',
        brief='Changes loungebot.cur_state',
        description='Changes cur_state to input. must be 0, 1, 2.'
    )
    async def change_cs(self, cxt: commands.Context, num):
        try:
            nxt = int(num)
            if nxt < 0 or 2 < nxt:
                raise ValueError
        except (IndexError, ValueError):
            cxt.channel.send('Need valid status number (0-2 int)')
            return

        cxt.bot.cogs['LoungeDoorStatus'].cur_status = nxt

    @commands.command(
        name='p'
    )
    async def new_inst(self, ctx):
        e = EmbedListPrinter(ctx)
        e.title = 'Emoji List'

        ids = [e.guild_id for e in ctx.bot.emojis]
        ids_order = sorted(set(ids))

        if ctx.guild.emojis:
            text = ''
            for m in ctx.guild.emojis:
                text += '{} `:{}:`\n'.format(str(m), m.name)
            for i in range(2):
                e.add_field(name='Server {} p{}'.format(ctx.guild.name, i), value=text)

        for i in ids_order:
            if i == ctx.guild.id:
                continue

            g = ctx.bot.get_guild(i)

            text = ''
            for m in g.emojis:
                text += '{} `:{}: | `:<{}>:`\n'.format(str(m), m.name, m.id)
            e.add_field(name='Server ' + g.name, value=text, inline=False)

        await e.send(ctx)
        ctx.bot.add_listener(e.change_page_listener, name='on_reaction_add')
