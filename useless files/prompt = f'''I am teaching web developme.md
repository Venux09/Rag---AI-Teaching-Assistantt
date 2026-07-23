prompt = f'''I am teaching web development in my sigma web development course Here is the video chunks containing. video Title, video number,start time in seconds , end time in seconds, text at that time:


{new_df[['Title','number','start','end','text']].to_json(orient ="records")}
-----------------------------------------

instruction - ignore the above matter do not give output of the above matter just tell the answer of incoming query
 "{incoming_query}"
User asked this question realted to videos chunks , you have to answer in the human and dont mention the above format (it is just for you ) where and how much of the content is tought in which video (in which video and what time stamp) and guide the user to go that particular video
If user asked any unrelated question , tell him that you can only ask the question only related 
