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
Here is example code for a barebones addon that replies `echoed xxx` when anyone sends `!echo xxx`.

```python
from discord.ext import commands
class PingPong(commands.Cog):
    @commands.command()
    async def echo(self, ctx, word):
        await ctx.send('echoed' + word)
```

Let's break this down line-by-line, because python is fucking magic.

```python
from discord.ext import commands
```
Import the discord command interface library. Easy enough.

```python
class PingPong(commands.Cog):
```
Define the Cog you are adding. The name will be the class name, in this case `PingPong`.
You can access this Cog using `client.get_cog('PingPong')`, allowing for inter-Cog communication.
The parenthesis are the python syntax for class inheritance.
The `commands.Cog` class handles all the behind-the-scenes magic, so the code you write can be linked to discord with a few simple lines.

```python
@commands.command()
```
This innocent-looking line handles almost all of the work behind the scenes.
The `@` denotes a [python decorator](https://realpython.com/primer-on-python-decorators/).
These are complicated, so all you need to know is that it will take the function you define on the next line,
and send it through several pipelines to connect it to the bot.
Also, note that there are parenthesis behind the line, meaning that `commands.command` is actually a function that returns a decorator.
You can put arguments in the parenthesis to do some cool stuff.

```python
async def echo(self, ctx, word):
```
Finally we get to defining the function we want to implement.
The `async` tag is necessary to define the function as a [coroutine](https://docs.python.org/3/library/asyncio-task.html). (Don't worry about it too much, this is just how discord.py works in the backend.)
The function's name `echo` defines how the command is called (`!echo`). To change this, pass a `name='something'` argument into the decorator above.
Lastly, the arguments of the command. `ctx` will be a [`Context`](https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#context) object that describes the message that triggered the command.
`word` is a magic [positional argument acceptor](https://discordpy.readthedocs.io/en/rewrite/ext/commands/commands.html#positional).

```python
await ctx.send('echoed' + word)
```
The actual code for the command is as simple or complex as you need it to be.
The `ctx.send` function sends a message back to the same channel that triggered the command.
It needs to be `await`'ed, because that's just how `discord.py` and coroutines work.
More discord commands can be found on the [API](https://discordpy.readthedocs.io/en/latest/api.html)

####Notes
I use a slightly different vocabulary from `discord.py`.
* `client` <-> `bot`
* `module` <-> `cog`