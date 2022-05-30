#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
import os
import json


def user_auth():
  """
  Either gets the email id and password from .env file or prompts input

  Returns:
    A tuple: (email, password)  
  """

  email = os.environ.get("EMAIL") or input("Enter Amazon Email: ")
  password = os.environ.get("PASSWORD") or getpass("Password: ")

  return (email, password)

def login(web):
  """
  Automates the login process

  Args:
    web: browser data type
  """

  user_login = user_auth()

  email = web.find_element(By.ID, "ap_email")
  email.clear()
  email.send_keys(user_login[0])

  password = web.find_element(By.ID, "ap_password")
  password.send_keys(user_login[1])

  sign_in_btn = web.find_element(By.ID, "signInSubmit")
  sign_in_btn.click()

def fetch_books(web):
  """
  Fetches all the books: h2 tags

  Args:
    web: browser

  Returns:
    A list of [<h2 nodes>]
  """
  books = web.find_elements(By.CSS_SELECTOR, "h2.kp-notebook-searchable")
  return books

def wait_payload(web, book, first, delay):
  try:
    loaded_book = WebDriverWait(web, delay).until(EC.element_to_be_clickable(book))
  except TimeoutError:
    print("Loading books took too much time to be clickable!")

  if not first: loaded_book.click()

  try:
    WebDriverWait(web, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#kp-notebook-annotations")))
  except TimeoutError:
    print("Loading notebook-annotations took too much time!")

  # Wait for AJAX requests to complete
  wait = WebDriverWait(web, delay)

  try:

    wait.until(lambda web: web.execute_script('return jQuery.active') == 0)
    wait.until(lambda web: web.execute_script('return document.readyState') == 'complete')

  except TimeoutError:
    print("Loading highlights took too much time!")


def fetch_highlights(web):
  """
  Fetches all the highlights from a given book. First clicks on the book, then waits for the notebook-annotations div to be present in the DOM, then wait for the Ajax request.

  Args:
    web: browser
    book: book element
  
  Returns:
    A list of highlights: [highlight1, highlight2, ...]
  """
  highlights = web.find_elements(By.ID, "highlight")

  # print(highlights, "\nNo. of highlights: ", len(highlights))

  annotations = []
  for high in highlights:
    high_text = high.text.strip()
    
    # Atleast 4 words in high_text
    if len(high_text.split()) > 3:
      annotations.append(high_text)

  return annotations


def unit_test():
  browser = webdriver.Firefox()
  browser.get("https://read.amazon.com/kp/notebook")

  login(browser)
  books = fetch_books(browser)
  # print(books)

  test0 = fetch_highlights(browser, books[0], True)
  print(test0,"\nNo. of highlights: ", len(test0)) # 192

  test1 = fetch_highlights(browser, books[1], False)
  print(test1,"\nNo. of highlights: ", len(test1)) # 60


def save_as_json(book_highlights, prog_dir):
  """
  Saves book_highlights to a json file

  Args:
    book_highlights: { book_name: [highlights] }
  """
  highlights_save_file_name = "highlights.json"

  with open(highlights_save_file_name, "w", encoding="utf-8") as f:
    json.dump(book_highlights, f, ensure_ascii=False, indent=2)

  save_file_path = os.path.join(prog_dir, highlights_save_file_name)
  print(f"Highlights Saved: {save_file_path}")


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

  book_highlights = {}

  for index, book in enumerate(books):
    is_first = False
    if index == 0:
      is_first = True

    wait_payload(browser, book, is_first, delay=100)
    highs = fetch_highlights(browser)

    # [atleast 1 highlight in the list]
    if highs:
      book_highlights[book.text.strip()] = highs

  # print(book_highlights)
  save_as_json(book_highlights, prog_dir)
  browser.close()

if __name__ == "__main__":
  print("Fetching data...")
  main()
