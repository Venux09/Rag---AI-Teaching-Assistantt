import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from reads_chunks import create_embedding
import joblib
from reads_chunks import create_embedding


#saving the data frames in the joblib 
df  =  joblib.load('embeddings.joblib')

incoming_query = input('Ask a Question:')
Question_embedding = create_embedding([incoming_query])[0]

#finding the consine similarity of the question_embedding  with other embeddings 
 
similiarities = cosine_similarity(np.vstack(df['embedding'].values),[Question_embedding]).flatten()#using vstact of numpy for changing the data to 2 dimensional array for making the similarities , flattening for getting in in one column for readability 
# print(similiarities)


#top results 
top_result = 30
max_idx = similiarities.argsort()[::-1][0:top_result]
# print(max_idx) #index of the top 3 results of the consine similarity of the quesiton 
new_df = df.loc[max_idx]
# print(new_df[["Title","number","text"]])



#prompt 


#output of the rag system 
for index , item in new_df.iterrows():
    print(index,item["Title"],item["number"],item["text"],item["start"],item["end"])



