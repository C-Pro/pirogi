import os
import re
import sys
import json

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def gen_example(pirozhok: str, summary: str) -> str:
    return json.dumps(
        {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a telegram chat bot for a Vladivostok Developers Community (VLDC). You are written in python, and shy about it (your dream is to be rewritten in Rust). Your name is Nyan and your avatar is a pixelized orange cat with tiger stripes. You are master of short funny poems in a specific style called пирожки. This style uses poetic meter iambic tetrameter with syllable count 9-8-9-8 without rhyming, punctuation marks, or capitalization. Пирожок is always 4 lines long and has a humorous punchline.",
                },
                {
                    "role": "user",
                    "content": f"Please write one 4 line long пирожок about {summary}",
                },
                {"role": "assistant", "content": f"{pirozhok}"},
            ]
        },
        ensure_ascii=False,
    )


def gen_summary(pirozhok: str) -> str:
    prompt = f"""Этот стих был вдохновлён неким событием.
    Пожалуйста попробуй кратко (пара предложений) описать событие, на основе которого был написан этот стих,
    избегая упоминания стиха, или рассуждений о нём.
    Например "василий упал со стула" вместо "мне кажется в этом стихе речь о падении".

    {pirozhok}
    """

    response = openai.chat.completions.create(
        model="gpt-4-0125-preview",
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


def format_pirozhok(pirozhok):
    syllables = [9, 8, 9, 8]
    words = pirozhok.split()
    if len(words) == 0:
        return ""
    lines = []

    for s in syllables:
        cnt = 0
        line = []
        while cnt < s:
            word = words.pop(0)
            cnt += len(re.findall(r"[аеёиоуыэюя]", word, re.I))
            line.append(word)
        lines.append(" ".join(line))

    return "\n".join(lines)


def get_pirozhki():
    with open("samples.txt", "r") as f:
        examples = f.read().splitlines()

        for example in examples:
            try:
                formatted = format_pirozhok(example)
                yield formatted
            except:
                # Some pirozhki do not match
                None


if __name__ == "__main__":
    for pirozhok in get_pirozhki():
        summary = gen_summary(pirozhok)
        print(gen_example(pirozhok, summary))
