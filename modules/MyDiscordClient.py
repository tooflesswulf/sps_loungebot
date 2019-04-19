import discord


class Client(discord.Client):
    cur_status = 2
    command_prefix = ''

    def freshcopy(self):
        new = Client(loop=self.loop)
        new.cur_status = self.cur_status
        new.command_prefix = self.command_prefix

        return new
