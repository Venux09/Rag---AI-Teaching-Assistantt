import requests #importing request module 
import os
import json
import time
import pandas as pd   
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity #scikit learn library for creating the cosine similarity of the  the arrays 


def create_embedding(text_list, retries=3):

    for attempt in range(retries):
        try:
            r = requests.post('http://localhost:11434/api/embed' ,
                            json={"model" : "nomic-embed-text",
                                  "input":text_list}, timeout=30)

            if r.status_code != 200:
                print(f"Attempt {attempt+1}: ERROR - {r.json()}")
                time.sleep(5)
                continue
            
            #creating the json of the embedding produced from the requested embedding
            embedding = r.json()["embeddings"]
            return embedding
        except Exception as e:
            print(f"Attempt {attempt+1}: Connection failed - {e}")
            if attempt < retries - 1:
                time.sleep(5)
            else:
                raise Exception(f"Ollama API failed after {retries} attempts: {e}")


#listing the json files 
jsons = os.listdir('jsons')
my_dicts = []
chunk_id = 0

for json_file in jsons : #json files in jsons
    try:
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
    except Exception as e:
        print(f"SKIPPED {json_file}: {e}")
        continue
    break


df = pd.DataFrame.from_records(my_dicts)#data frame of the dictionary of the chunks 
print(df)
incoming_query = input('Ask a Question:')
Question_embedding = create_embedding([incoming_query])[0]



#finding the consine similarity of the question_embedding  with other embeddings 
 
similiarities = cosine_similarity(np.vstack(df['embedding'].values),[Question_embedding]).flatten()#using vstact of numpy for changing the data to 2 dimensional array for making the similarities , flattening for getting in in one column for readability 
print(similiarities.argsort())
print(similiarities)


