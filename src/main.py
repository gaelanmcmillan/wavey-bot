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
    print(f"Logged in as {bot.user.name}")


# ┌──────────────┐
# │ Bot Commands │
# └──────────────┘

@client.command(name="ping")
async def SendMessage(ctx):
    await ctx.send("pong")

if __name__ == "__main__":
    client.run(TOKEN)
