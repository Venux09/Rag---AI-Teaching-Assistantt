import whisper
import json

model = whisper.load_model("small")#Loading whisper Large-v2 model for turning billingual mp3 to Text 

#transribing the audio to text - uhh language of the video - hindi and task is to translate that to english
result = model.transcribe(audio="audios/16_Exercise 1 - Solution & Shoutouts .mp3",
                          language ="hi",
                          task='translate'
                          )


print(result["text"])#model generated result 
# with open("output.json","w") as f :
#     json.dump(f,result)




