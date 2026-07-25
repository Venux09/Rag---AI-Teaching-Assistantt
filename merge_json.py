import os #operating system 
import json #json 
import math  # mathmatics module 

n = 5 #converting 1 chunks into 1 

for filename in os.listdir('jsons'):#listing the filenames from the json folders 
    if filename.endswith('.json'):
        file_path = os.path.join('jsons',filename)#join the path of json folder with its files 
        with open(file_path,'r',encoding='utf-8') as f:
            data = json.load(f) #loading the file paths means json golder in the data variable 
            new_chunks = []
            num_chunks = len(data['chunks']) #lenght of the number of the chunk in the files 
            num_groups = math.ceil(num_chunks/n)

            for i in range(num_groups):#taking iteration for the range in num_groups 
                start_idx =  i*n  #give the number which was from the start called num _chunks as it cancel out the n 
                end_idx = min((i+1)*n ,num_chunks)#taking the mininmum between these two 

                chunk_group  = data['chunks'][start_idx:end_idx]
 

                new_chunks.append({
                    "number":data['chunks'][0]['number'],
                    "Title":chunk_group[0]['Title'],
                    "start":chunk_group[0]['start'],
                    "end":chunk_group[-1]['end'],
                    "text":"".join( c['text'] for c in chunk_group )                   
                })
            #saving this file without double json 
            os.makedirs('new_json',exist_ok=True)#making a new directory named as new_json
            with open(os.path.join("new_json",filename),'w',encoding='utf-8') as json_file:
                json.dump({'chunks':new_chunks,'text': data['text']},json_file,indent=4)




