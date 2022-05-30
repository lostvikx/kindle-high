#!/usr/bin/env python3

from fetch import login, fetch_books, wait_payload
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
import os
import json


def fetch_highlight_divs(web):
  
  highlight_divs = web.find_elements(By.CSS_SELECTOR, ".a-row.a-spacing-base > .a-column.a-span10.kp-notebook-row-separator")

  print(len(highlight_divs))


def main():
  load_dotenv(find_dotenv())

  prog_dir = os.environ.get("KINDLE_HIGH")
  os.chdir(prog_dir)

  browser = webdriver.Firefox()
  browser.get("https://read.amazon.com/kp/notebook")

  # Wrong email or password
  while True:
    login(browser)
    books = fetch_books(browser)

    if len(books):
      break
    else:
      print("Login failed! Wrong email or password.")
      continue

  for index, book in enumerate(books):
    is_first = False
    if index == 0:
      is_first = True

    # [atleast 1 highlight in the list]
    wait_payload(browser, book, is_first, 100)
    highs = fetch_highlight_divs(browser)

if __name__ == "__main__":
  main()
