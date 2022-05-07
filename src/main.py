import os

from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands

import cogs.testcog

load_dotenv()

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
TS_GUILD_ID = os.getenv("TS_GUILD_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!")

# ┌──────────────────┐
# │ Start-up Routine │
# └──────────────────┘

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}") #TODO: formalize a logging solution instead of printing to standard out


# ┌──────────────┐
# │ Bot Commands │
# └──────────────┘

@client.command(name="ping")
async def SendMessage(ctx):
    await ctx.send("pong")

@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice)

if __name__ == "__main__":
    client.run(TOKEN)
