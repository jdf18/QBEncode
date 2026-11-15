from pathlib import Path
from typing import Optional

WORDS_PATH = Path("durhack_word_list.csv")

def get_words() -> list[str]:
    with open(WORDS_PATH) as file:
        lines = file.readlines()
    return lines

def str_to_int(inp: str) -> Optional[int]:
    return 0

def int_to_str(inp: int) -> str:
    return ""
