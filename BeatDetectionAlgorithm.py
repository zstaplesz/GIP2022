import librosa
from matplotlib import pyplot as plt
import numpy as np
import serial
import os
import time
import statistics
import PredictedBeats
os.getcwd()

# Activates Arduino if connected, COM4 requires an update to COM port of Arduino (see Ardruino IDE documentation)

playback = False
try:
    ser = serial.Serial('COM4',9600)
    playback = True
except:
    com = 'plot'

######################################################################################################################
# Song sample and threshold specification, of the 3 samples provided, uncomment choice.

AudioFile = '_Piano_1.wav'
PredictedSampleTimes = PredictedBeats.PredictedPiano1Ear
AvStr = 1.1435298715166289

# AudioFile = '_Drum_1.wav'
# PredictedSampleTimes = PredictedBeats.PredictedDrum1Ear
# AvStr = 2.5718054305762053

# AudioFile = '_Full_Song_2_Cut.wav'
# PredictedSampleTimes = PredictedBeats.PredictedFullSong2Ear
# AvStr = 1.664127558279429

######################################################################################################################

# Extracting audio sample information and normalising
x, sr = librosa.load(AudioFile)
times = np.arange(len(x))/float(sr)
x = x/max(x)


# Onset detection calculation
onset_times = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1, delta=0.028, units='time')



# Decomposed onset detection calcuation strengths and times respectively
onset_strengths = librosa.onset.onset_strength(y=x, sr=sr)
onse_times = librosa.times_like(onset_strengths)


# Tempo detection calculation
tempo, beat_times = librosa.beat.beat_track(y=x, sr=sr, units='time')


######################################################################################################################
# Filtering - decomposed onset detection peak picking algorithm
StrengthTimes = []
StrengthFiltered = []
StrFilFil = []
StrTimeFil = []
TempStr = []
TempTime = []


onse_strengths = onset_strengths
onset_strengths = onset_strengths.tolist()


# Alternative threshold determination methods; general and statistical respectively

# AvStr = 2.3
# AvStr = 2*statistics.mean(onset_strengths)


for i in range(len(onset_strengths)):
    if onset_strengths[i] <= AvStr:
        onset_strengths[i] = 0
    if onset_strengths[i] > AvStr:
        StrengthTimes.append(onse_times[i])
        StrengthFiltered.append(onset_strengths[i])

for i in range(len(onset_strengths)):
    if onset_strengths[i] != 0:
        TempStr.append(onset_strengths[i])
    if onset_strengths[i] == 0:
        if TempStr:
            StrFilFil.append(max(TempStr))
            StrTimeFil.append(onse_times[onset_strengths.index(max(TempStr))])
        TempStr = []


######################################################################################
# Assigning strengths to percentiles

q5, q4, q3, q2, q1 = np.percentile(StrFilFil, [90,80,70,60,50])
AdaStr = []
for i in range(len(StrFilFil)):
    if StrFilFil[i] >= q5:
        AdaStr.append('1\n')
    elif StrFilFil[i] >= q4:
        AdaStr.append('2\n')
    elif StrFilFil[i] >= q3:
        AdaStr.append('3\n')
    elif StrFilFil[i] >= q2:
        AdaStr.append('7\n')
    elif StrFilFil[i] >= q1:
        AdaStr.append('8\n')
    else:
        AdaStr.append('9\n')

#####################################################################################
# Beat detection mode selection - setting output to Arduino to decomposed onset detection, no user input required
ChosenMethodList = StrTimeFil
#####################################################################################

# If Arduino is connected, this will send the beat information and actuation will occur

PlayLoop = True
if playback == True:
    while PlayLoop == True:

        com = input("Press Enter to continue, or type 'end' to quit, or 'plot' to plot graphs and quit.")
        if com == 'end' or com == 'plot':
            PlayLoop = False
            break

        SongStartTime = time.perf_counter()
        for i in range(len(ChosenMethodList)):
            Current_Time = time.perf_counter()
            SongTime = Current_Time - SongStartTime
            while SongTime < ChosenMethodList[i]:
                Current_Time = time.perf_counter()
                SongTime = Current_Time - SongStartTime
            ser.write(str.encode(AdaStr[i]))





#######################################################################################
# Plotting


if com == 'plot':

    # Plotting beats detected for all methods (ignoring strengths)

    fig1 = plt.figure(1)
    fig1.set_size_inches((12, 4))

    BeatMag = []
    OnsetMag = []
    StrMag = []
    for b in range(len(beat_times)):
        BeatMag.append(-0.1)
    for o in range(len(onset_times)):
        OnsetMag.append(-0.2)
    for s in range(len(StrTimeFil)):
        StrMag.append(-0.3)

    plt.scatter(beat_times, BeatMag, color='m',label='BPM Detection', zorder=5)
    plt.scatter(onset_times, OnsetMag,  color='g',label='Onset Detection', zorder=5)
    plt.scatter(StrTimeFil, StrMag,  color='r',label='Decomposed Onset Detection', zorder=5)

    plt.scatter([],[], color='k', label='Estimation by Ear', zorder=10)
    for xc in PredictedSampleTimes:
       plt.axvline(x=xc, color='k')

    plt.plot(times, x, color='c', zorder=0)
    plt.scatter([], [], color='c', label='Time Series Audio Data', zorder=0)
    plt.title("Beats Detected from Different Methods \n" + str(AudioFile))

    plt.xlabel('Time (s)')
    plt.ylabel('Magnitude')

    plt.legend(loc='upper right')

    # Plotting strength peaks and beats detected, the onset peaks are normalised for plotting purposes only

    maxStr = max(StrFilFil)
    for i in range(len(StrFilFil)):
        StrFilFil[i] = StrFilFil[i]/maxStr

    maxOS = max(onset_strengths)
    for i in range(len(onset_strengths)):
        onset_strengths[i] = onset_strengths[i]/maxOS

    maxONS = max(onse_strengths)
    for i in range(len(onse_strengths)):
        onse_strengths[i] = onse_strengths[i]/maxONS


    fig2 = plt.figure(2)
    fig2.set_size_inches((4, 4))
    plt.plot(times, x, color='c')
    plt.scatter([], [], color='c', label='Time Series Audio Data', zorder=0)
    plt.plot(onse_times, onset_strengths, color='b')
    plt.scatter([], [], color='b', label='Filtered Onset Strength Envolope')
    plt.scatter(StrTimeFil, StrFilFil, color='r', label='Detected Beats', zorder = 10)
    plt.legend(loc="lower left")
    plt.xlabel('Time (s)')
    plt.ylabel('Magnitude')

    plt.show()



