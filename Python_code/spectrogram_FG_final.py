

import librosa, librosa.display
from matplotlib import pyplot as plt
import numpy as np
import os
import csv
from itertools import zip_longest


### FOLDER WHERE THE AUDIO (WAV) ARE
AUDIO_DATABASE = "D:/Neuroscience/Forrest Gump/ad-av/av/audio/Seg99"  # --> add path for the relevant folder

FULLaudio = "D:/Neuroscience/Forrest Gump/ad-av/av/audio/fg_av_ger_seg99.wav"
### FOLDER WHERE THE SPECTROGRAM ARE/WILL GO  
SPECTRO_PATH = "D:/Neuroscience/Forrest Gump/ad-av/Spectrogram analysis" # --> add path for the relevant folder

### Function generating a spectrogram
def spectrogram_stft(data_path, plot=False):
   
    ### Compute and plot STFT spectrogram for database
    ### sampling point, sample rate = audio file path
    data, sr = librosa.load(os.path.join(data_path), sr=None, duration = None)    
            
    # Perform different STFT depending of the sample rate
    
    if sr == 44100:
       
        stft2 = np.abs(librosa.stft(data, n_fft=4096, window='hann', win_length=4096, hop_length=2048))
      
        
        print("Sample rate is 44100")
        
        if plot == True:
            plt.figure(figsize=(10, 5))
            plt.subplot(211)
            plt.title("Spectrogram STFT")
            librosa.display.specshow(librosa.amplitude_to_db(stft2, ref=np.max), y_axis='linear', x_axis='time', cmap='hot', sr=sr)
            
    
            
            
        return stft2
    elif sr == 22050:
    
        stft2 = np.abs(librosa.stft(data, n_fft=2048, window='hann', win_length=2048, hop_length=1024))
        
        print("Sample rate is 22050")

      
        if plot == True:
            plt.figure(figsize=(10, 5))
            plt.subplot(211)
            plt.title("Spectrogram STFT")
            librosa.display.specshow(librosa.amplitude_to_db(stft2, ref=np.max), y_axis='linear', x_axis='time', cmap='hot', sr=sr)
            
        return stft2

        
def reducedstfts(audiofile):

    stft1 = np.array(spectrogram_stft(audiofile, plot = False)) ### --> CHANGE THIS TO PLOT OR NOT
    print("STFT performed on whole audio")
        
    #Frequency bands
    third = int(len(stft1)/3)
    #print(third)
    
    #LOW
    freqLow = stft1[:len(stft1)-(2*third)]    
    sumLow = np.sum(freqLow, axis=0).tolist()
        
       
    #MID
    freqMid = stft1[len(stft1)-(2*third):len(stft1)-third]
    sumMid = np.sum(freqMid, axis=0).tolist()  
    # print("Midfreq = ", sumMid)
    
    #HIGH
    freqHigh = stft1[len(stft1)-third:len(stft1)]
    sumHigh = np.sum(freqHigh, axis=0).tolist()
    # print("Highfreq = ", sumHigh)
    
    ##concatenate to 1 value per freq band:
    sumLow = np.sum(sumLow)
    sumMid = np.sum(sumMid)
    sumHigh = np.sum(sumHigh)
    #print("this is concatenated low freq: ", sumLow)
    
    #COMBINE
    threebands = (
           sumLow,
           sumMid,
           sumHigh
           ) ## separate each sum variable with [] if arrays rather than single values in order to create list of arrays
    
    
    print("Combined into 3 freq bands: ", threebands)
    print("\nLow", threebands[0], "\nMid ", threebands[1],"\nHigh ", threebands[2], "\n")
    
    return threebands      


class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)
    #def __str__(self):
       # return str(self.__class__) + ": " + str(self.__dict__) # if needed for variable printing, not in this case
stfts = GrowingList()

### Function going through each wav file of a folder a generating a spectrogram 
def spectrogram_maker(database_path, spectrogram_path):
    stfts = GrowingList()
    counter = -1
   
    duration = int(librosa.get_duration(filename=FULLaudio)) #calculates audiofile segment duration in seconds
    nbfiles= int(duration / 4) #acquires number of chunked audio files for a given segment
    print("### Spectrogram creation done... ###\n")
    for j in range(0, nbfiles):
        for i in range(4000, 0, -1000): #4000 is audio chunk length in ms
    # Goes through each file path to create a spectrogram
           for file in (file for file in os.scandir(database_path) if file.name == ("fg_av_ger_seg99_%s_chunk%s.wav" % (i, j))):

                   if file.name[:-4] == ".mkv":
                       continue
                
                   print("Analysing file: ", file.name)
 
                   counter += 1     #tells how many seconds analyzed 
                   
                   print("The counter: ", counter)
                                           
                        # Creating a STFT + filter for the loaded database file
                   redst = reducedstfts(file)
                   #print("this is reduced stft of audio file: ", redst.shape)
                   print("before append: ", stfts)
                   
                        
                   stfts[counter] = redst
                        #print(stfts)
                   print("added a new stft to list: ", len(stfts))
    final_spec3 = list(stfts)
    return final_spec3
    
                
final_spec = spectrogram_maker(AUDIO_DATABASE, SPECTRO_PATH)  

path = "D:/Neuroscience/Forrest Gump/ad-av/"

        #### SAVE TO .csv ####
export_data = zip_longest(*final_spec, fillvalue = '')
with open((path + 'spectro_99credits.csv'), 'w', encoding="ISO-8859-1", newline='') as f: 
    write = csv.writer(f) 
    #write.writerow(final_spec) # have arrays as column titles 
    write.writerows(export_data) # nb of columns corresponds to final counter value
f.close()
        
print("### Spectrogram creation starts... ###\n")