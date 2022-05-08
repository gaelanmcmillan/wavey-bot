- set up a virtual environment with `virtualenv wavey-bot` in terminal
- installed nextcord in the environment with `python3 -m pip install -U "nextcord[voice]"` in terminal
- to update requirements.txt, use the terminal command `pip freeze > requirements.txt`





### Nextcord related notes:
Regarding declaring new bot commands, there seems to be two ways to declare a command that sends a message. I'm not sure what the difference is.

```py
client = nextcord.ext.commands.Bot()

# These two ways of defining a "ping pong" command seem to be equivalent.

@client.command(name="ping")
async def SendMessage(ctx):
    await ctx.send("pong")

@client.command()
async def ping(ctx):
    await ctx.send("pong")
```

I'm not sure what the difference between these two approaches is, or which is superior.