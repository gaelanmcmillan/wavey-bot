"""
Use librosa to manipulate audio wave form and play back locally with simpleaudio.
"""

#https://librosa.org/doc/latest/auto_examples/plot_audio_playback.html#sphx-glr-auto-examples-plot-audio-playback-py
import librosa as lbr
import numpy as np
#https://simpleaudio.readthedocs.io/en/latest/simpleaudio.html
import simpleaudio as sa

# included audio sample
path = lbr.example('trumpet')

# load an audio file as a floating point time series
# y = np darray: audio time series
# sr = sampling rate
y, sr = lbr.load(path)

# play audio from time series
# (audio data, num. audio channels, bytes per single channel sample, sampling rate)
play = sa.play_buffer(y, 1, 4, sr)

play.wait_done()