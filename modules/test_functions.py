from discord.ext import commands
from modules.embed_printer import EmbedPrinter


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
        name='create'
    )
    async def new_inst(self, ctx, num):
        add = EmbedPrinter(ctx.bot, num)
        ctx.bot.add_cog(add)
