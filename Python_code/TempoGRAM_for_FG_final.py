# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 12:59:13 2021

@author: Leo
"""



import librosa, librosa.feature, librosa.display
import numpy as np
import os
import csv

### FOLDER WHERE THE AUDIO (WAV) ARE
AUDIO_DATABASE = "D:/Neuroscience/Forrest Gump/ad-av/av/audio/Seg99"  # --> add path for the relevant folder

FULLaudio = "D:/Neuroscience/Forrest Gump/ad-av/av/audio/fg_av_ger_seg99.wav"
### FOLDER WHERE THE SPECTROGRAM ARE/WILL GO  
SPECTRO_PATH = "D:/Neuroscience/Forrest Gump/ad-av/Spectrogram analysis" # --> add path for the relevant folder



def tempogram_perform(data_path, plot = True):
    data, sr = librosa.load(os.path.join(data_path), sr=None, duration = None)    
    print("audio sample array: ", data.shape)


    oenv = librosa.onset.onset_strength(y=np.asarray(data))

    # Estimate the global tempo for display purposes
    
    tempo = librosa.beat.tempo(onset_envelope=oenv, sr=sr,
    
                               hop_length=512)[0]


    print("this chunk has a tempo of: ", tempo)
    return tempo

class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)
 
tempi = GrowingList()

### Function going through each wav file of a folder a generating a spectrogram 
def tempogram_maker(database_path, spectrogram_path):
    tempi = GrowingList()
    counter = -1
   
    duration = int(librosa.get_duration(filename=FULLaudio)) #calculates audiofile segment duration in seconds
    nbfiles= int(duration / 4) #acquires number of chunked audio files for a given segment
    print("### Tempogram creation done... ###\n")
    for j in range(0, nbfiles): #nbfiles
        for i in range(4000, 0, -1000): #4000 is audio chunk length in ms
    # Goes through each file path to create a spectrogram
           for file in (file for file in os.scandir(database_path) if file.name == ("fg_av_ger_seg99_%s_chunk%s.wav" % (i, j))):

                   if file.name[:-4] == ".mkv":
                       continue
                
                   print("Analysing file: ", file.name)
 
                   counter += 1     #tells how many seconds analyzed 
                   
                   print("The counter: ", counter)
                   
                # Making sure hidden files are not considered
                        
                        # Creating a STFT + filter for the loaded database file
                   tempo_data = round(tempogram_perform(file)) ### --> CHANGE THIS TO PLOT OR NOT
                   print("Tempogram performed on whole audio")
                   #print("this is reduced stft of audio file: ", redst.shape)
                   print("novel tempo: ", tempo_data)
                   
                        #arr = np.zeros((nb_rows, int(len(redst)))) #creates arrays of 0 of hop_length row, and nb_rows being 
                        
                   tempi[counter] = tempo_data
                        #print(stfts)
                   print("added a new TEMPO to list of length: ", len(tempi))
    final_tempi3 = np.array(tempi)
    print(final_tempi3)
    return final_tempi3

                
final_tempi = tempogram_maker(AUDIO_DATABASE, SPECTRO_PATH)  

path = "D:/Neuroscience/Forrest Gump/ad-av/"

        #### SAVE TO .csv ####

with open((path + 'tempo_9credits.csv'), 'w', encoding="ISO-8859-1", newline='') as f: 
    write = csv.writer(f) 

    write.writerow(final_tempi) # nb of columns corresponds to final counter value, i.e. number of seconds analyzed
f.close()


print("### Tempogram creation starts... ###\n")

