import requests #importing request module 
import os
import json
import pandas as pd   
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity #scikit learn library for creating the cosine similarity of the  the arrays 
import joblib #for saving the data frames 

def create_embedding(text_list):#function for creating the embedings
        #creating the embedding using the nomic-emebed for creating the embeddings 
        
            r = requests.post('http://localhost:11434/api/embed' ,
                            json={"model" : "bge-3m",
                                  "input":text_list})

            #creating the json of the embedding produced from the requested embedding
            embedding = r.json()["embeddings"]
            return embedding


#listing the json files 
jsons = os.listdir('jsons')
jsons.sort(key=lambda x: int(x.split('_')[0]))  # Sort by number at start (1, 2, 3... 10, 11)

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


df = pd.DataFrame.from_records(my_dicts)#data frame of the dictionary of the chunks 


#saving the dataframe using joblib
joblib.dump(df,"embeddings.joblib")



