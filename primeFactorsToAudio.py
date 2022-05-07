import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt 
import soundfile as sf
import math



def primefactors(n):
    p_l = []
    #even number divisible
    while n % 2 == 0:
        p_l.append(2)
        n = n / 2
    
   #n became odd
    for i in range(3,int(math.sqrt(n))+1,2):
     
        while (n % i == 0):
            p_l.append(int(i))
            n = n / i
    
    if n > 2:
        p_l.append(int(n))
    return p_l
 

def func(t, f):
    return np.sin(t * f* 2 * np.pi)

def func_list(t, f_list):
    val = 0
    for f in f_list:
        val += func(t, f)
    return val
def Split(l, n):
    l = list(l)
    while len(l) % n != 0:
        l.pop()
    x = list(np.split(np.array(l), n))
    
    return [list(v) for v in x]

def SimultaneusAudio(t_list, frequency_list):
    note_l = []
    for t in t_list:
        val = func_list(t, frequency_list)  
        note_l.append(val)
    return np.array(note_l)

def NonSimultaneusAudio(t_list, frequency_list):
    note_l = []
    num_freq = len(frequency_list)
    split_t = Split(t_list, num_freq)
    for i in range(num_freq):
        for t in split_t[i]:
            val = func(t, frequency_list[i])
            note_l.append(val)
    return np.array(note_l)

def GetTimeList(audio_length, sampling_rate):
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t_list = np.linspace(0, audio_length, audio_length * sampling_rate, False)
    return t_list

def GetFrequencyList(n, scale_v):
    p_factors = primefactors(n)
    print(p_factors)
    frequency_list = list(np.array(p_factors) * scale_v)
    return frequency_list

def PlayAudio(note, sampling_rate):
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback

    play_obj = sa.play_buffer(audio, 1, 2, sampling_rate)

    # Wait for playback to finish before exiting
    play_obj.wait_done()
    return audio

def PlotAudio(t_list, note):
    plt.plot(t_list, note)
    plt.show()

def SaveAudioAsWav(file_name, audio, sampling_rate):
    sf.write(file_name, audio, sampling_rate, 'PCM_24')

#initial conditions:
n = 2*2*3*5*7*11*13*17*23*29*123*200
scale_v = 50
audio_length = 5 #s
sampling_rate = 44100


# either NonSimultaneusAudio or SimultaneusAudio

note = NonSimultaneusAudio(GetTimeList(audio_length, sampling_rate), GetFrequencyList(n, scale_v))


audio = PlayAudio(note, sampling_rate)

#SaveAudioAsWav("audio.wav", audio, sampling_rate)


