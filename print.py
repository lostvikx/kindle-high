#!/usr/bin/env python3

from argparse import ArgumentParser
import json
from random import choice
import subprocess
import os
from dotenv import load_dotenv, find_dotenv
import re


def parse_highlights(book_highlights):
  """
  Parses highlights into all_annotations and book_names

  Args:
    book_highlights: { "book_name": [ ...highlights ] }

  Returns:
    Random (all_annotation: [ ..."highlight ~ book_name" ], book_names: [ ...book_name ])
  """

  all_annotations = []
  book_names = list(book_highlights.keys())

  for book_name, highlights in book_highlights.items():
    for high in highlights:
      all_annotations.append(f"{high} ~ {book_name}")

  return (all_annotations, book_names)


def parse_args():
  """
  Helper fn: provides --help and --update-highlights flags.

  Returns:
    args: object
  """
  parser = ArgumentParser(description="Print a random annotation from your kindle highlights")

  parser.add_argument("-u", "--update-highlights", help="update the annotations by running fetch.py", action="store_true")

  parser.add_argument("-b", "--book-name", help="get annotation from specific book")

  args = parser.parse_args()
  return args


def main():
  load_dotenv(find_dotenv())

  highlights_save_file_name = "highlights.json"
  needs_fetch = False
  
  # Change directory
  prog_dir = os.environ.get("KINDLE_HIGH")
  os.chdir(prog_dir)

  try:
    with open(highlights_save_file_name, "r", encoding="utf-8") as f:
      data = json.load(f)
      all_annotations, book_names = parse_highlights(book_highlights=data)

  except FileNotFoundError:
    print(f"{highlights_save_file_name} not found!")
    needs_fetch = True
    pass
  except Exception as err:
    print(f"Something went wrong: {err}")

  if parse_args().update_highlights or needs_fetch:
    print("Updating highlights.json...")
    try:
      # subprocess.run(["python3", "fetch.py"])
      pass
    except Exception as err:
      print(f"Couldn't run fetch.py: {err}")

  # Print annotation from a specific book 
  elif parse_args().book_name:
    book_name = parse_args().book_name

    matches = []
    for name in book_names:
      if re.search(book_name, name, re.I):
        matches.append(name)

    if len(matches) == 1:
      book_title = matches[0]
      annotation = choice(data[book_title])
      print(f"{annotation} ~ {book_title}")

    # Multiple matches
    elif matches:
      print(matches)
      while True:
        try:
          select_book = int(input("Enter index of book: "))
        except Exception:
          print("Please enter a number!")
          continue

        try:
          book_title = matches[select_book]
          annotation = choice(data[book_title])
          print(f"{annotation} ~ {book_title}")
          break
        except IndexError:
          print("Please enter a valid index value!")
          continue
        except Exception as err:
          print(f"Something went wrong: {err}")
          break

  else:
    annotation = choice(all_annotations)
    try:
      print(annotation)
    except Exception as err:
      print(f"Couldn't print highlight: {err}")


if __name__ == "__main__":
  main()
