#!/usr/bin/env python3

import json
from random import choice

def main():
  highlights_save_file_name = "highlights.json"

  with open(highlights_save_file_name, "r", encoding="utf-8") as f:
    data = json.load(f)
    books = list(data.keys())
    selected_book = choice(books)

    high = choice(data[selected_book])
    print(f"{high} ~ {selected_book}")

if __name__ == "__main__":
  main()
