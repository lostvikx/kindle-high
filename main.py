#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
import os
from time import sleep

load_dotenv(find_dotenv())

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

def fetch_highlights(web, book, first):
  """
  Fetches all the highlights from a given book. First clicks on the book, then waits for the notebook-annotations div to be present in the DOM, then wait for the Ajax request.

  Args:
    web: browser
    book: book element
  
  Returns:
    A list of highlights: [highlight1, highlight2, ...]
  """
  delay = 100

  try:
    loaded_book = WebDriverWait(web, delay).until(EC.element_to_be_clickable(book))
  except TimeoutError:
    print("Loading books took too much time to be clickable!")

  if not first: loaded_book.click()

  try:
    WebDriverWait(web, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#kp-notebook-annotations")))
  except TimeoutError:
    print("Loading notebook-annotations took too much time!")

  # Subject to change!
  # sleep(10)
  # highlights = web.find_elements(By.ID, "highlight")

  try:
    highlights = WebDriverWait(web, delay).until(lambda doc: doc.find_elements(By.ID, "highlight"))
  except TimeoutError:
    print("Loading highlights took too much time!")

  print(highlights, "\nNo. of highlights: ", len(highlights))

  # annotations = []
  # for high in highlights:
  #   high_text = high.text.strip()
  #   if len(high_text.split()) > 3:
  #     annotations.append(high_text)

  # return annotations

  # return [high.text.strip() for high in highlights]

def main():
  browser = webdriver.Firefox()
  browser.get("https://read.amazon.com/kp/notebook")

  login(browser)
  books = fetch_books(browser)
  # print(books)

  book_highlights = {}

  # Testing
  test0 = fetch_highlights(browser, books[0], True)
  # print(test0,"\nNo. of highlights: ", len(test0)) # 192

  # test1 = fetch_highlights(browser, books[1], False)
  # print(test1,"\nNo. of highlights: ", len(test1)) # 60

  # for index, book in enumerate(books):
  #   is_first = False
  #   if index == 0:
  #     is_first = True
    
  #   book_highlights[book.text.strip()] = fetch_highlights(browser, book, is_first)

  # print(book_highlights)


if __name__ == "__main__":
  main()
