#!/usr/bin/env python3

from argparse import ArgumentParser
import json
from random import choice
import subprocess
import os
from dotenv import load_dotenv, find_dotenv


def select_annotation(book_highlights)->str:
  """
  Select a random highlight

  Args:
    book_highlights: { "book_name": [ ...highlights ] }

  Returns:
    Random annotation, a string, "highlight ~ book_name"
  """
  all_annotations = []
  for book_name, highlights in book_highlights.items():
    for high in highlights:
      all_annotations.append(f"{high} ~ {book_name}")

  return choice(all_annotations)

def parse_args():
  """
  Helper fn: provides --help and --update-highlights flags.

  Returns:
    args: object
  """
  parser = ArgumentParser(description="Print a random annotation from your kindle highlights")

  parser.add_argument("-u", "--update-highlights", help="Update the annotations by running fetch.py", action="store_true")

  args = parser.parse_args()
  return args


def main():
  load_dotenv(find_dotenv())

  highlights_save_file_name = "highlights.json"
  needs_fetch = False
  
  prog_dir = os.environ.get("KINDLE_HIGH")
  os.chdir(prog_dir)

  try:
    with open(highlights_save_file_name, "r", encoding="utf-8") as f:
      data = json.load(f)
      annotation = select_annotation(book_highlights=data)
  except FileNotFoundError:
    print(f"{highlights_save_file_name} not found!")
    needs_fetch = True
    pass
  except Exception as err:
    print(f"Something went wrong: {err}")

  if parse_args().update_highlights or needs_fetch:
    print("Updating highlights.json...")
    subprocess.run(["python3", "fetch.py"])
  
  try:
    print(annotation)
  except Exception as err:
    print(f"Couldn't print highlight: {err}")


if __name__ == "__main__":
  main()
