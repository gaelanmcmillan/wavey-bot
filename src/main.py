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

async def play_audio_file(file_path: str, ctx) -> None:

    voice_client = nextcord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice_client is None:
        voice_client = await ctx.message.author.voice.channel.connect()

    if not voice_client.is_playing():
        source = nextcord.FFmpegPCMAudio(file_path)
        player = voice_client.play(source)
    else:
        voice_client.pause()
        await play_audio_file(file_path, ctx)

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

    await ctx.send(f"Let's hear '{input_string}'")
    
    wav_path: str = await generate_wav_from_primes(input_string)
    if wav_path:
        await play_audio_file(wav_path, ctx)
    else:
        await ctx.send("could not generate a wav file from {input_string}")

# ┌──────────────┐
# │ Random Chord │
# └──────────────┘

def prettify_chord_name(file_name: str) -> str:
    return file_name.replace('_', ' ')[:-4]

def generate_guess_options(file_name: str, chords_dir: str, number_of_options: int) -> list[str]:
    chord_files = list(filter(lambda s: s.startswith(file_name[0]), os.listdir(chords_dir)))
    selections = [file_name]
    while (len(selections) < number_of_options):
        new_idx = randint(0, len(chord_files)-1)
        candidate = chord_files[new_idx]
        if candidate not in selections:
            selections.append(chord_files[new_idx])

    print("Final selections: ", selections)
    return selections

def select_random_chord(chords_dir: str) -> str:
    chord_files = list(filter(lambda s: s!=".DS_Store", os.listdir(chords_dir)))
    selection_idx = randint(0, len(chord_files)-1)
    path_of_chosen_chord = chord_files[selection_idx]
    print(f"Selected chord: '{path_of_chosen_chord}'")
    chord_name = prettify_chord_name(path_of_chosen_chord)
    return chord_name, os.path.join(CHORDS_DIR, path_of_chosen_chord)

@client.command(
    name="chord",
    pass_context=True
)
async def random_chord(ctx):
    # active_voice_client = nextcord.utils.get(client.voice_clients, guild=ctx.guild)

    chord_name, path_of_chosen_chord = select_random_chord(CHORDS_DIR)

    await ctx.send(f"Let's hear... {chord_name}")

    await play_audio_file(path_of_chosen_chord, ctx)

# ┌───────────────────┐
# │ Ear Training Game │
# └───────────────────┘

@client.command(name="guess")
async def play_guess_chord(ctx):
    await ctx.send("""Starting a new game of ***Guess the Chord***, where everything is a chord and the points don't matter!""")

    chord_name, chord_path = select_random_chord(CHORDS_DIR)
    # active_voice_client = nextcord.utils.get(client.voice_clients, guild=ctx.guild)

    view = nextcord.ui.View()

    async def play_chord_callback(interaction: nextcord.Interaction):
        await play_audio_file(chord_path, ctx)
        await interaction.response.edit_message(view=view) # we reset the view so the button is clickable again

    play_button = nextcord.ui.Button(label="▶︎", style=nextcord.ButtonStyle.green)
    play_button.callback = play_chord_callback
    view.add_item(play_button)

    option_count = 6
    guess_options = list(map(prettify_chord_name, generate_guess_options(chord_path[7:], CHORDS_DIR, option_count)))
    print(f"Guess the Chord | Answer: {chord_name}, Options: {guess_options}")

    winning_pos = randint(0, option_count-1)

    print("winning chord is ", chord_name, " winning pos is ", winning_pos)
    guess_options[0], guess_options[winning_pos] = guess_options[winning_pos], guess_options[0]
    print(guess_options)
    guess_buttons = [nextcord.ui.Button(label=chord, style=nextcord.ButtonStyle.blurple, custom_id=str(i)) for i, chord in enumerate(guess_options)]

    async def submit_guess_callback(interaction: nextcord.Interaction, button: nextcord.ui.Button):
        print(button.custom_id)

        for b in guess_buttons:
            b.disabled = True

        print(f"Custom id: {button.custom_id} winning pos: {str(winning_pos)} id==pos? {button.custom_id==str(winning_pos)}")
        if button.custom_id == str(winning_pos):
            for b in guess_buttons:
                if b.custom_id != button.custom_id: b.style = nextcord.ButtonStyle.gray
                else: b.style = nextcord.ButtonStyle.green
            await interaction.response.edit_message(content=f"YES! The chord was ***{button.label}***", view=view)
        else:
            for b in guess_buttons:
                if b.custom_id == str(winning_pos): b.style = nextcord.ButtonStyle.blurple
                elif b.custom_id != button.custom_id: b.style = nextcord.ButtonStyle.gray
                else: b.style = nextcord.ButtonStyle.red
            await interaction.response.edit_message(content=f"Aww... Sorry, the correct answer was ***{chord_name}***. Better luck next time!", view=view)

    def curry_in_button(func, button):
        return lambda interaction: func(interaction, button)

    for button in guess_buttons:
        button.callback = curry_in_button(submit_guess_callback, button)
        view.add_item(button)

    await ctx.send("***Guess the Chord***", view=view)
    result = await view.wait()
    print("Results: ", result)

if __name__ == "__main__":
    client.run(TOKEN)
