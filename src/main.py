import os
import asyncio
from random import randint
from discord import Interaction

from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands

import cogs.testcog

from primeFactorsToAudio import generate_wav_from_primes 

load_dotenv()

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
TS_GUILD_ID = os.getenv("TS_GUILD_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
CHORDS_DIR = os.getenv("CHORDS_DIR")

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!")

# ┌──────────────────┐
# │ Start-up Routine │
# └──────────────────┘

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}") #TODO: formalize a logging solution instead of printing to standard out



# ┌──────────────────┐
# │ Helper Functions │
# └──────────────────┘

def play_audio_file(file_path: str) -> None:
    source = nextcord.AudioSource(file_path)


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
        active_voice_client = await channel.connect()
        # source = nextcord.FFmpegPCMAudio('test.wav')
        # player = active_voice_client.play(source)
    else:
        await ctx.send("You must be in a voice channel to run this command.")

@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I'm not in a voice channel")


# ┌────────────────────────────────────────────┐
# │ Strats Prime Factorization Sound Generator │
# └────────────────────────────────────────────┘

@client.command(
    name="play_primes",
    pass_context=True
)
async def play_primes(ctx, input_string: str=None):

    if input_string is None:
        input_string = ctx.message.author.name

    active_voice_client = nextcord.utils.get(client.voice_clients, guild=ctx.guild)
    if not active_voice_client:
        active_voice_client = await ctx.message.author.voice.channel.connect()

    await ctx.send(f"Let's hear '{input_string}'")
    
    wav_path: str = await generate_wav_from_primes(input_string)
    if wav_path:
        source = nextcord.FFmpegPCMAudio(wav_path)
        player = active_voice_client.play(source)
    else:
        await ctx.send("could not generate a wav file from {input_string}")

# ┌──────────────┐
# │ Random Chord │
# └──────────────┘

def select_random_chord(chords_dir: str) -> str:
    chord_files = list(filter(lambda s: s!=".DS_Store", os.listdir(chords_dir)))
    selection_idx = randint(0, len(chord_files)-1)
    path_of_chosen_chord = chord_files[selection_idx]
    print(f"Selected chord: '{path_of_chosen_chord}'")
    prettified_chord_name = path_of_chosen_chord.replace('_', ' ')[:-3]
    return prettified_chord_name, os.path.join(CHORDS_DIR, path_of_chosen_chord)

@client.command(
    name="chord",
    pass_context=True
)
async def random_chord(ctx):
    active_voice_client = nextcord.utils.get(client.voice_clients, guild=ctx.guild)

    if not active_voice_client:
        active_voice_client = await ctx.message.author.voice.channel.connect()

    if active_voice_client.is_playing():
        active_voice_client.pause()
        active_voice_client.source.clean_up()

    chord_name, path_of_chosen_chord = select_random_chord(CHORDS_DIR)

    await ctx.send(f"Let's hear... {chord_name}")

    source = nextcord.FFmpegPCMAudio(path_of_chosen_chord)
    player = active_voice_client.play(source)
    print("type of player: ", type(player))

if __name__ == "__main__":
    client.run(TOKEN)
