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
async def internal_function(ctx):
    await ctx.send("pong")

@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = nextcord.FFmpegPCMAudio('test.wav')
        player = voice.play(source)
    else:
        await ctx.send("You must be in a voice channel to run this command.")

@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I'm not in a voice channel")

if __name__ == "__main__":
    client.run(TOKEN)
