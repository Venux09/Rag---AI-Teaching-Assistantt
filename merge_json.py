import os 
import json 
import math 

n = 5

for filename in os.listdir('jsons'):
    if filename.endswith('.json'):
        file_path = os.path.join('jsons',filename)
        with open(file_path,'r',encoding='utf-8') as f:
            data = json.load()
            new_chunks = []
            num_chunks = len(data['chunk'])
            num_groups = math.ceil(num_chunks/n)

            for i in range(num_groups):
                start_idx =  i*n
                end_idx = min((i+1)*n,new_chunks)

                chunk_group  = data['chunks'][start_idx:end_idx]


                new_chunks.append({
                    "number":data['chunks'][0]['number'],
                    "Title":data['chunks'][0]['Title'],
                    "start":data['chunks'][0]['start'],
                    "end":data['chunks'][-1]['end']
                   
                })