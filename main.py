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

def fetch_highlights(web, book):
  """
  Fetches all the highlights from a given book

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

  loaded_book.click()

  try:
    WebDriverWait(web, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#kp-notebook-annotations")))
  except TimeoutError:
    print("Loading notebook-annotations took too much time!")

  # Subject to change!
  sleep(10)
  highlights = web.find_elements(By.ID, "highlight")
  # print(highlights, "\nNo. of highlights: ", len(highlights))

  return [high.text.strip() for high in highlights]

def main():
  browser = webdriver.Firefox()
  browser.get("https://read.amazon.com/kp/notebook")

  login(browser)
  # book_names, books = fetch_books(browser)
  books = fetch_books(browser)

  book_highlights = {}

  # Testing
  # test1 = fetch_highlights(browser, books[0])
  # print(test1,"\nNo. of highlights: ", len(test1) )

  for book in books:
    # fetch_highlights(browser, book)
    book_highlights[book.text.strip()] = fetch_highlights(browser, book)

  print(book_highlights)


if __name__ == "__main__":
  main()
