import whisper
import json
import os

model = whisper.load_model("small")#Loading whisper Large-v2 model for turning billingual mp3 to Text 


audios = os.listdir("audios")#listing the audios folder - of all mp3 

#transribing the audio to text - uhh language of the video - hindi and task is to translate that to english
for audio in audios:
    if("_" in audio):
        number = audio.split("_")[0]#numbers of the tutorial
        title = audio.split("_")[1][:-4]#title of the tutorial excluding the mp3
        print(number,title)
        result = model.transcribe(audio=f"audios/{audio}",
                                language ="hi",
                                task='translate',
                                  word_timestamps= False
                                )
        

        chunks = []#chunks of the output/result produced by the model 
        for  segment in result["segments"]:#getting segment out of the result produced by the model 


            #appending segments and other info to the chunks 
            chunks.append({"number":number,"Title":title,"start":segment["start"],"end":segment["end"],"text":segment["text"]})#appending the empty chunks list to the segment [from the result]


        #chunks with the metadata 
        chunks_with_metadata = {"chunks":chunks,"text":result["text"]}


        with open(f"jsons/{audio}.json","w") as f : #loading the chunks into the json file - jsons/files 
            json.dump(chunks_with_metadata,f)     

            