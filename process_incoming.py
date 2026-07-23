import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from reads_chunks import create_embedding
import joblib
from reads_chunks import create_embedding
import pandas as pd 
import requests

#inference 
def inference(prompt):#loading the model for the generation 

       r = requests.post('http://localhost:11434/api/generate',
       json={"model" : "llama3.2:1b",
       "prompt":prompt,
       "stream":False})


       response = r.json()
       print(response)
       return response





#saving the data frames in the joblib 
df =  joblib.load('embeddings.joblib')

incoming_query = input('Ask a Question:')
Question_embedding = create_embedding([incoming_query])[0]

#finding the consine similarity of the question_embedding  with other embeddings 
 
similiarities = cosine_similarity(np.vstack(df['embedding'].values),[Question_embedding]).flatten()#using vstact of numpy for changing the data to 2 dimensional array for making the similarities , flattening for getting in in one column for readability 
# print(similiarities)


#top results 
top_result = 5 
max_idx = similiarities.argsort()[::-1][0:top_result]
# print(max_idx) #index of the top 3 results of the consine similarity of the quesiton 
new_df = df.loc[max_idx]
# print(new_df[["Title","number","text"]])



#prompt 
prompt = f"""
You are an AI Teaching Assistant for the Sigma Web Development Course.

Course Context:
{new_df[['Title','number','start','end','text']].to_json(orient='records')}

User Question:
{incoming_query}

Instructions:
- Answer ONLY using the provided course context.
- If the answer exists, respond naturally as a teacher.
- Mention:
  • Video number
  • Video title
  • Relevant timestamp(s)
  • What is taught at those timestamps.
- If the topic appears in multiple timestamps or videos, combine them into one concise answer.
- Guide the user to watch the most relevant video and timestamp first.
- Do NOT mention "chunks", "context", "retrieved data", "JSON", or any internal processing.
- Do NOT explain how you found the answer.
- Do NOT add unnecessary headings or extra text.
- If the question is unrelated to the Sigma Web Development Course, reply exactly:
  "I can only answer questions related to the Sigma Web Development Course."
- If the provided course content does not contain the answer, reply:
  "I couldn't find this topic in the available course videos."
- Keep the response concise, helpful, and human-like.
"""

response = inference(prompt)['response']
print(response)

with open ('response.txt',"w") as f :
    f.write(response)



#output of the rag system 
# for index , item in new_df.iterrows():
#     print(index,item["Title"],item["number"],item["text"],item["start"],item["end"])





