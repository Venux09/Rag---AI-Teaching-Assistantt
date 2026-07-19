import whisper
import json

model = whisper.load_model("small")#Loading whisper Large-v2 model for turning billingual mp3 to Text 

#transribing the audio to text - uhh language of the video - hindi and task is to translate that to english
result = model.transcribe(audio="audios/16_Exercise 1 - Solution & Shoutouts .mp3",
                          language ="hi",
                          task='translate',
                          word_timestamps= False
                          )


print(result["segments"])#model generated result 

chunks = []#chunks of the output produced by the model 
for  segment in result["segments"]:#getting segment out of the result produced by the model 
    chunks.append({"start":segment["start"],"end":segment["end"],"text":segment["text"]})#appending the empty chunks list to the segment [from the result]


print(chunks)

with open ("output.json","w") as f : #loading the chunks into the json file - output.json 
    json.dumps(chunks,f)