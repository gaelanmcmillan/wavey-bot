#from re import L
import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt 
import soundfile as sf
import math
from datetime import datetime

import asyncio



async def generate_wav_from_primes(input_str):

    def primefactors(n):
        if n < 2:
            return []
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
    
    def stepFunc(t, a, c):
        return 2 * a * np.sin((t - c) * a)/((t - c) * a)

    def stepFuncList(t_list, a, c):
        v_list = []
        for t in t_list:
            val = stepFunc(t, a, c)
            v_list.append(val)
        return v_list

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

    def GenerateAudio(t_list, frequency_list):
        note_l = []
        num_freq = len(frequency_list)
        split_t = Split(t_list, num_freq)
        for i in range(num_freq):
            for t in split_t[i]:
                val = func(t, frequency_list[i])
                note_l.append(val)
        

        note_all = AddBeat(num_freq, note_l, t_list, audio_length)
        return np.array(note_all)

    def AddBeat(beat_f, values, t_list, audio_length):

        if (1/beat_f) >= audio_length:
            print("too low beat")
            return values 


        width = 0.0001
        amp = 0.4
        temp = PeaksFunc(t_list, audio_length, 1/beat_f, width, amp)
        # plt.plot(temp[0], temp[1])
        # plt.show()

        peak_f_list = temp[1]
        #print("p1", len(t_list), len(values), len(peak_f_list))
        res = []

        for (item1, item2) in zip(values, peak_f_list):
            res.append(item1+item2)

        return res

    def PeaksFunc(t_list, total_time,T, width, amp):
        t_list = list(t_list)
        res = []
        p_n = 0
        num_per_s = len(t_list)/total_time
        peaks = []
        p = 0


        while t_list[p] < t_list[-1]:
            peaks.append(t_list[p])
            p +=int( num_per_s * T)
            if p > len(t_list) - 1:
                break
        
        #print("peaks", peaks)


        p_n = 1
        p_tot = len(peaks)
        i = 0
        # print("width", width)
        # print(len(t_list))
        # print("peaks", peaks)
        # print("peaks 0", peaks[p_n])
        while p_n < p_tot :
            while t_list[i] < (peaks[p_n] - width):
                res.append(0)
                #print("MMM", i)
                i += 1
            if p_n == p_tot - 1:
                while t_list[i] < (peaks[p_n]):
                    #print("OOO", i)
                    res.append(amp)
                    i += 1
            else:

                while t_list[i] < (peaks[p_n] + width):
                    #print("LLL", i)
                    res.append(amp)
                    i += 1
                
            p_n += 1
        
        return [t_list[:len(res)], res]

    def GetTimeList(audio_length, sampling_rate):
        # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
        t_list = np.linspace(0, audio_length, audio_length * sampling_rate, False)
        return t_list

    def GetFrequencyList(n, scale_v, numFunc):
        p_factors = numFunc(n)
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

    def PlotAudio(audio):
        plt.plot(audio[1], audio[0])
        plt.show()

    def SaveAudioAsWav(file_name, audio, sampling_rate):
        sf.write(file_name, audio, sampling_rate, 'PCM_16')

    def TextToNum1(str):
        num = 0
        for c in str:
            #print(c, ord(c))
            num += ord(c)
        #print(num)
        return num

    def TextToNum2(str):
        num = 1
        for c in str:
            #print(c, ord(c))
            num *= ord(c)
        #print(num)
        return num



    try:
        n = int(input_str)

    except:
        n = TextToNum1(input_str)
    if n < 2:
        return ""


    #initial conditions:

    scale_v = 30.868 #wanted pitch
    audio_length = 5#s 
    sampling_rate = 44100

    note = GenerateAudio(GetTimeList(audio_length, sampling_rate), GetFrequencyList(n, scale_v, primefactors))

    #audio = PlayAudio(note, sampling_rate)

    now = datetime.now()
    addon = str(now)[-3:]
    date_time = now.strftime("%d-%m-%Y-%H-%M-%S") + "-" + addon

    file_name = "PrimeFactorizationFile" + date_time + ".wav"
    SaveAudioAsWav(file_name, note, sampling_rate)
    print(f"generated file as {file_name}")
    return file_name


