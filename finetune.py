import os
import sys
import pickle
import json
import datetime

import openai

SKIP=5

if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()
    files = json.load(open("files.json", "rt"))
    files.sort(key=lambda x: x["name"])

    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    if month == 8:
        file = files[SKIP+day-28]
    elif month == 9:
        if day > 23:
            raise ValueError("September 23 is the last day of free fine-tuning")
        file = files[SKIP+4+day]
    else:
        raise ValueError("September 23 is the last day of free fine-tuning")

    print(file["id"])

    last_job = client.fine_tuning.jobs.list().data[0]
    print(last_job.fine_tuned_model)

    res = client.fine_tuning.jobs.create(
        training_file=file["id"],
        validation_file="file-w09YKYO4REdmxo5b8ZDZau99",
        model=last_job.fine_tuned_model
    )

    print(res)
