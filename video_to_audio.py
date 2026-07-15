#changin Video to audio 
import os 
import subprocess #used for running program from python itself 


files = os.listdir('videos')#listing the videos files in videos folder 
for file in files:
    tutorials_numbers = file.split(" - CodeWithHarry")[0].split(" #")[1] #splitting the Tutorial number out of the video 
    file_name = file.split(" Sigma")[0] # file names of the course videos
    print(tutorials_numbers,file_name)
    #subprocess - will run the ffmpeg in terminal for all the fiels one by one 
    subprocess.run(["ffmpeg","-i",f"videos/{file}",f"audios/{tutorials_numbers}_{file_name}.mp3"])

