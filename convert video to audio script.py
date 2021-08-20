
import moviepy
import os
import moviepy.editor 
import glob

pathdir = "D:/Neuroscience/Forrest Gump/ad-av/av/"

# Get a list of all the files with .mkv extension in pathdir folder.
list_folder=glob.glob(os.path.join(pathdir, "*.mkv"))
dirnames = "D:/Neuroscience/Forrest Gump/ad-av/av/"

for filename in list_folder:

         print(filename)
        
         # save file to some directory on disk
        
         video = moviepy.editor.VideoFileClip(filename)
         audio = video.audio
         
         if audio is not None:
             wav_filename = filename.replace(".mkv", ".wav")
             audio.write_audiofile(wav_filename)
             
    
else:
            print("Finished conversion of Forrest Gump")
    



