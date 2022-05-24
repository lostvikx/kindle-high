#!/usr/bin/env python3

import json
from random import choice

def select_annotation(book_highlights):
  all_annotations = []
  for book_name, highlights in book_highlights.items():
    for high in highlights:
      all_annotations.append(f"{high} ~ {book_name}")

  print(choice(all_annotations))

def main():
  highlights_save_file_name = "highlights.json"

  try:
    with open(highlights_save_file_name, "r", encoding="utf-8") as f:
      data = json.load(f)
      select_annotation(book_highlights=data)
  except FileNotFoundError:
    print(f"{highlights_save_file_name} not found!")
  except Exception as err:
    print(f"Something went wrong: {err}")


if __name__ == "__main__":
  main()
