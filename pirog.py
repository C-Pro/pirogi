import os
import sys
import pickle
import json

import openai

def walk_files_in_dir(directory):
    import os
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def read_data_file(file):
    with open(file, 'rb') as openfile:
        data = pickle.load(openfile)
    return data

def gen_example(pirozhok: str, summary: str) -> str:
    return json.dumps(
        {
            "messages": [
                {
                    "role": "system",
                    "content": "Ты чат бот владивостокского коммьюнити разработчиков VLDC. Ты написан на python но в тайне хотел бы переписать себя на rust. Тебя зовут Нян и твой аватар это пиксельный оранжевый кот с тигриными полосками. Ты мастер коротких забавных (часто саркастических) стихов в стиле пирожок. Этот стиль использует метрику ямбического тетраметра с количеством слогов 9-8-9-8 без рифмы, знаков препинания или заглавных букв. Пирожок всегда состоит из 4 строк.",
                },
                {
                    "role": "user",
                    "content": f"Пожалуйста, напиши 4-х строчный стишок-пирожок, основываясь на тексте следующего параграфа:\n\n{summary}",
                },
                {"role": "assistant", "content": f"{pirozhok}"},
            ]
        },
        ensure_ascii=False,
    )

def gen_summary(pirozhok: str) -> str:
    prompt = f"""Перескажи содержание текста в следующем параграфе,
    избегая дословного цитирования и любых вступлений вида "в этом тексте идёт речь о", "в стихотворении говорится" или рассуждений о нём.
    Например "василий упал со стула" вместо "мне кажется в этом стихе речь о падении" или "в стихотворении идёт речь о падении со стула".
    Используй исключительно русский язык.

    {pirozhok}
    """
    client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    response = client.chat.completions.create(
        #model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
        model="lmstudio-community/gemma-2-9b-it-GGUF",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.5,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    totalCnt = 40561
    cnt = 0
    skip = 34875
    for file in walk_files_in_dir("./pages"):
        for pirog in read_data_file(file):
            cnt += 1
            if cnt < skip:
                continue
            summary = gen_summary(pirog)
            print(gen_example(pirog, summary))
            if cnt % 10 == 0 and cnt > 0:
                pcnt = float(cnt) / float(totalCnt) * 100.0
                print(f"{pcnt:.2f}% done ({cnt} of {totalCnt})", file=sys.stderr)
