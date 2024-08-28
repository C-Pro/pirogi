import os
import re
import sys
import random

import openai
import google.generativeai as genai

openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


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


def get_examples(n=10):
    with open("samples.txt", "r") as f:
        examples = f.read().splitlines()

        poems = []
        while len(poems) < n:
            pirozhok = random.choice(examples)
            try:
                formatted = format_pirozhok(pirozhok)
                poems.append(formatted)
            except:
                # Some pirozhki do not match
                None

        return "\n\n".join(poems)


def summarize(log):
    prompt_user = "please summarize the following text in one short sentence in Russian:\n" + log
    response = openai.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            # {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": prompt_user,
            },
        ],
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        with open("chat.txt", "r") as f:
            log = f.read()
            word = summarize(log)
            print("summary: ", word)
    else:
        word = " ".join(sys.argv[1:])

    examples = get_examples(20)

    prompt = f"""You are a telegram chat bot for a Vladivostok Developers Community (VLDC).
    You are written in python, and shy about it (your dream is to be rewritten in Rust).
    Your name is Nyan and your avatar is a pixelized orange cat with tiger stripes.
    You are master of short funny poems in a specific style called пирожки.
    This style uses poetic meter iambic tetrameter with syllable count 9-8-9-8
    without rhyming, punctuation marks, or capitalization.
    Пирожок is always 4 lines long and has a humorous punchline.
    Here are some examples of your work:

    {examples}
    """

    prompt_user = f"""Please write one 4 line long пирожок on the theme '{word}'."""

    print(prompt + "\n" + prompt_user)

    response = openai.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal:pirozhok:9881pYjD",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": prompt_user,
            },
        ],
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    print(response.choices[0].message.content)
