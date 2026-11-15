from pathlib import Path
from typing import Optional

WORDS_PATH = Path("durhack_word_list.csv")

def get_words() -> list[str]:
    with open(WORDS_PATH) as file:
        lines = file.readlines()
    return list(map(str.strip, lines))

def str_to_int(inp: str) -> Optional[int]:
    for char in inp:
        if char not in "qwertyuiopasdfghjklzxcvbnm-":
            return None

    parts = inp.split("-")
    if len(parts) != 3:
        return None

    w1, w2, w3 = parts

    words = get_words()

    c1 = words.index(w1)
    c2 = words.index(w2)
    c3 = words.index(w3)

    return c1 + (2**15 * c2) + (2**30 * c3)

def int_to_str(inp: int) -> str:
    div, c1 = divmod(inp, 2**15)
    div, c2 = divmod(div, 2**15)
    div, c3 = divmod(div, 2**15)

    words = get_words()

    w1 = words[c1]
    w2 = words[c2]
    w3 = words[c3]
    return f"{w1}-{w2}-{w3}"

if __name__ == "__main__":
    for i in range(10):
        inp = int_to_str(i)
        check = str_to_int(inp)
        print(f"{i}, {inp}, {check}")
