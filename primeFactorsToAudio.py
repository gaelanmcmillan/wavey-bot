import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt 
import soundfile as sf
import math


n = 24
scale_v = 50


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


p_factors = primefactors(n)
print(p_factors)
frequency_list = list(np.array(p_factors) * scale_v)  # Our played note will be 440 Hz

#print(frequency_list)


fs = 44100  # 44100 samples per second
seconds = 1  # Note duration of 3 seconds



# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t_list = np.linspace(0, seconds, seconds * fs, False)


note_l = []
for t in t_list:
    val = func_list(t, frequency_list)  
    note_l.append(val)

note = np.array(note_l)


# plt.plot(t_list, note)
# plt.show()


# Ensure that highest value is in 16-bit range
audio = note * (2**15 - 1) / np.max(np.abs(note))
# Convert to 16-bit data
audio = audio.astype(np.int16)

# Start playback

play_obj = sa.play_buffer(audio, 1, 2, fs)

# Wait for playback to finish before exiting
play_obj.wait_done()


#To save the audio as .wav:
#sf.write('audioFile.wav', audio, fs, 'PCM_24')

