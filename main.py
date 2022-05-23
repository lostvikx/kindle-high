#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
import os

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
    web: browser session data type
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
  """
  books = web.find_elements(By.CSS_SELECTOR, "h2.kp-notebook-searchable")

  # book_names = [book.text.strip() for book in books]
  print(f"No. of boooks: {len(books)}")

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
  pass

def main():
  browser = webdriver.Firefox()
  browser.get("https://read.amazon.com/kp/notebook")

  login(browser)
  fetch_books(browser)


if __name__ == "__main__":
  main()
