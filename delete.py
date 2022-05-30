#!/usr/bin/env python3

from fetch import user_auth, login, fetch_books
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
import os
import json

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

if __name__ == "__main__":
  main()
