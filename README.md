# sps_loungebot

A discord bot for Purdue SPS lul. I should probably create a devel branch or something.

### Dependencies

**Written on Python 3.7.1**. Use on other versions at your own risk. (it'll probably work lmao)

* [discord.py](https://github.com/Rapptz/discord.py) (Requires python 3.5.3)
* [numpy](https://www.numpy.org/)

### Features
Thus far, the following list of features have been implemented:

* Budget Nitro - lets anyone use animated emojis.
* Lounge status - indicates whether the lounge door is open or closed.


### How this Works
A basic understanding of Python is required to add features to this bot.

The bot runs using `discord.py`'s command extension module, which is well documented [here](https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html).
A simple example is shown [here](https://github.com/Rapptz/discord.py#bot-example).

We use a slightly more advanced method of organization, `Cogs`. [documentation here](https://github.com/Rapptz/discord.py#bot-example).
Each `Cog`, stored under [modules](modules/), is a class that wraps several related functions and can keep track of local fields.
Here is example code for a barebones addon that replies `pong` when anyone sends `ping`.

```python
from discord.ext import commands
class PingPong(commands.Bot):
    @commands.command()
    async def ping(self, ctx):
        ctx.send('pong')
```


####Notes
I use a slightly different vocabulary from `discord.py`.
* `client` <-> `bot`
* `module` <-> `cog`