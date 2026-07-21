import os
import json

json_dir = "jsons"
files = [f for f in os.listdir(json_dir) if f.endswith(".json")]

for file in files:
    filepath = os.path.join(json_dir, file)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Filter out missing or completely empty text chunks
    if "chunks" in data and isinstance(data["chunks"], list):
        data["chunks"] = [
            c for c in data["chunks"] 
            if isinstance(c, dict) and str(c.get("text", "")).strip()
        ]
        
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

print("🎉 All JSON files cleaned and stripped of empty text chunks!")
