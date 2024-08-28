import json

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

f = open('examples.jsonl', 'r')
for line in f.readlines():
    o = json.loads(line)
    summary = o['messages'][1]['content'][len("Please write one 4 line long пирожок about "):]
    pirozhok = o['messages'][2]['content']

    print(gen_example(pirozhok, summary))
