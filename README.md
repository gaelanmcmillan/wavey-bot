<img src="wavey.png" width="150"/>

# Wavey
A discord bot specializing in interactive audio experiences!
(As of the current version, Wavey only really specializes in playing local .WAV files. That's OK, Wavey. We're still proud of you)


### Installation

[FFmpeg](https://ffmpeg.org/) is required for Wavey to stream audio in discord voice channels. Head on over to the [FFmpeg download page](https://ffmpeg.org/download.html) and select the installation for your operating system, or use a command line utility of your choice. [FFmpeg is on homebrew](https://formulae.brew.sh/formula/ffmpeg), [chocolatey](https://community.chocolatey.org/packages/ffmpeg) and [Linux package managers](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu).

### Documentation

#### Commands
+ `join` - Make Wavey join your current voice channel.
+ `leave` - Make Wavey leave your current voice channel.
+ `play_prime <optional: input_string>` - Synthesize audio from the input string (if none is provided, your username is used). Audio automatically plays in the current voice channel.
+ `chord` - Play a random chord in the current voice channel.

### References
- [nextcord](https://pypi.org/project/nextcord/) - A Python wrapper for the discord.js API. See the [documenation](https://docs.nextcord.dev/en/latest/api.html#).
- [ffmpeg](https://ffmpeg.org/) - A complete, cross-platform solution to record, convert and stream audio and video. Necessary for streaming audio in discord voice channels.