import requests #importing request module 
import os
import json

def create_embedding(text_list):

#requesting bge-m3 to create embedding from the prompt we have given 
    r = requests.post('http://localhost:11434/api/embed' ,
                    json={"model" : "bge-m3",
                    "input":text_list})


    #creating the json of the embedding produced from the requested embedding 
    embedding = r.json()['embedding']
    
    #returning embedding from the text 
    return embedding



#listing the json files 
jsons = os.listdir('jsons')
my_dict = []
chunk_id = 0
for json_file in jsons : #json files in jsons
    with open(f"jsons/{json_file}") as f :
        content = json.load(f)#loaing the content of the json file 
    embeddings = create_embedding[{c["text"] for c in content['chunks']}] #create the embedding of the Text block of the json files 

    for chunk in content['chunks']: # json content chunks as chunk
        print(chunk)
        chunk['chunk_id'] = chunk_id #id of the chunk of the json
        chunk['embedding'] = create_embedding(chunk['text']) #settng chunk embedding as the embedding of the text in the chunk blocks
        chunk_id += 1
        my_dict.append('chunk')

    break
    


