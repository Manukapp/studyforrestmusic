
##SPLICING INTO 4s wavs##


from pydub import AudioSegment
from pydub.utils import make_chunks
import os, glob
audio_path = "D:/Neuroscience/Forrest Gump/ad-av/av/audio/"
for file in glob.glob(os.path.join(audio_path, "*.wav")):

    myaudio = AudioSegment.from_file(file, "wav") 
    chunk_length_ms = 4 * 1000 # pydub calculates in millisec
    overlap = 1000 #window sliding
    
    #print(len(myaudio))
  
    #Dividing the audiofile into 4 second chunks 
    #Second iteration starts chunking 1 second further (sliding window or overlap)
    #Third iteration 2 seconds further, Fourth iteration 3 seconds further 
    #And stops (as 4 seconds up is the same as first iteration but omitting first 4 seconds of audio)

    for i in range(chunk_length_ms, 0, -1000):
        myaudio = AudioSegment.from_file(file, "wav") 
        
        myaudio = myaudio[(chunk_length_ms - i):len(myaudio)]
        
        print("this is iterative i: ", i)
        print(len(myaudio))
        chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 4 sec, but starting at 1s further
        

        for j, chunk in enumerate(chunks):
            chunked_name = "_%s_chunk%s.wav" % (i, j)
            chunk_name = file[:-4] + chunked_name
            print("exporting", chunk_name)
            chunk.export(chunk_name, format="wav")
