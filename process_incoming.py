import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from reads_chunks import create_embedding
import joblib
import requests




def create_embedding(text_list, ):#function for creating the embedings 
        
        #creating the embedding using the nomic-emebed for creating the embeddings 
    
            r = requests.post('http://localhost:1234/v1/embeddings' ,
                            json={"model" : "lm-kit/bge-m3-gguf",
                                  "input":text_list})
            #creating the json of the embedding produced from the requested embedding
            print(r.status_code)
            
            response = r.json()
            if "error" in response:
                   print(response["error"])
                   return None
            return [data['embedding']for data in response["data"] ]

#saving the data frames in the joblib 
df  =  joblib.load('embeddings.joblib')

incoming_query = input('Ask a Question:')
Question_embedding = create_embedding([incoming_query])[0]

#finding the consine similarity of the question_embedding  with other embeddings 
 
similiarities = cosine_similarity(np.vstack(df['embedding'].values),[Question_embedding]).flatten()#using vstact of numpy for changing the data to 2 dimensional array for making the similarities , flattening for getting in in one column for readability 
print(similiarities)

top_result = 3
max_idx = similiarities.argsort()[::-1][0:top_result]
print(max_idx) #index of the top 3 results of the consine similarity of the quesiton 


new_df = df.loc[max_idx]
print(new_df[["Title","number","text"]])


