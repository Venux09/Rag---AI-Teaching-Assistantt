import requests #importing request module 
import os
import json
import pandas as pd   
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity #scikit learn library for creating the cosine similarity of the  the arrays 


def create_embedding(text_list):

#requesting bge-m3 to create embedding from the prompt we have given 
    r = requests.post('http://localhost:11434/api/embed' ,
                    json={"model" : "bge-m3",
                          "input":text_list})


    #creating the json of the embedding produced from the requested embedding
    embedding = r.json()["embeddings"]
    
    #returning embedding from the text 
    return embedding


#listing the json files 
jsons = os.listdir('jsons')
my_dicts = []
chunk_id = 0

for json_file in jsons : #json files in jsons
    with open(f"jsons/{json_file}") as f :
        content = json.load(f)#loaing the content of the json file which is as f 

    print(f"Creating embeddings for the {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])


    #create the embedding of the Text block of the json files 
    for i , chunk in enumerate(content['chunks']): # json content chunks as chunk
        chunk['chunk_id'] = chunk_id #id of the chunk of the json
        chunk['embedding'] = embeddings[i] #settng chunk embedding as the embedding of the text in the chunk blocks
        chunk_id += 1
        my_dicts.append(chunk) 
        if i == 5:
            break
    break


df = pd.DataFrame.from_records(my_dicts)#data frame of the dictionary of the chunks 
print(df)
incoming_query = input('Ask a Question:')
Question_embedding = create_embedding([incoming_query])[0]
print(Question_embedding)


#finding the consine similarity of the question_embedding  with other embeddings 
 
similiarities = cosine_similarity(np.vstack(df['embedding'].values),[Question_embedding])#using vstact of numpy for changing the data to 2 dimensional array for making the similarities


