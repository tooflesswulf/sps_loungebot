from discord.ext import commands
import discord


class EmbedListPrinter(commands.Cog):
    def __init__(self, ctx, max_len=20):
        self.bot = ctx.bot
        self.author = ctx.author
        self.max_len = max_len

        self.fields = []
        self.page_len = 0
        self.pages = []
        self.page_no = 0

        self.title = None
        self.msg = None

    def add_field(self, name='', value='', inline=False):
        v_len = value.count('\n') + 1
        if v_len + self.page_len <= self.max_len:
            self.fields.append((name, value, inline))
            self.page_len += v_len
            if self.page_len == self.max_len:
                self.page_len = 0
                self.pages.append(len(self.fields))
            return

        stop_line = self.max_len - self.page_len - 1
        text = value.split('\n')
        self.fields.append((name, '\n'.join(text[:stop_line]), inline))

        self.pages.append(len(self.fields))
        self.fields.append((name, '\n'.join(text[stop_line:]), inline))
        self.page_len = v_len - stop_line

    async def send(self, ctx):
        if self.page_len != 0:
            self.pages.append(len(self.fields))

        start_tmp = 0
        for i, end_num in enumerate(self.pages):
            self.pages[i] = slice(start_tmp, end_num)
            start_tmp = end_num

        e = discord.Embed(title=self.title)
        for name, value, inline in self.fields[self.pages[self.page_no]]:
            e.add_field(name=name, value=value, inline=inline)
        e.set_footer(text='Page {}/{}'.format(1+self.page_no, len(self.pages)))
        self.msg = await ctx.send(embed=e)

        if len(self.pages) != 1:
            discord.utils.get(ctx.bot.emojis, name='⬅')
            await self.msg.add_reaction('⬅')
            await self.msg.add_reaction('➡')

    async def change_page_listener(self, rxn, user):
        if len(self.pages) == 1 or user != self.author:
            return
        if rxn.emoji == '⬅':
            await rxn.remove(user)
            if self.page_no == 0:
                return

            self.page_no -= 1
        elif rxn.emoji == '➡':
            await rxn.remove(user)
            if self.page_no+1 == len(self.pages):
                return

            self.page_no += 1
        else:
            return

        e = discord.Embed(title=self.title)
        for name, value, inline in self.fields[self.pages[self.page_no]]:
            e.add_field(name=name, value=value, inline=inline)
        e.set_footer(text='Page {}/{}'.format(1+self.page_no, len(self.pages)))
        await self.msg.edit(embed=e)
