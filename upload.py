import os
import sys
import json

import openai

def walk_parts():
    import os
    for root, dirs, files in os.walk("split"):
        for file in files:
            if file.endswith(".jsonl") and file.startswith("part"):
                yield os.path.join(root, file)

if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()
    files = []
    for part in walk_parts():
        res = client.files.create(file=open(part, 'rb'), purpose='fine-tune')
        files.append({"id": res.id, "name": res.filename})
    json.dump(files, sys.stdout, ensure_ascii=False)
