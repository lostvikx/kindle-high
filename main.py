#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def user_auth():
  email = os.environ.get("EMAIL") or input("Enter Amazon Email: ")
  password = os.environ.get("PASSWORD") or getpass("Password: ")

  return (email, password)

def login(web):
  user_login = user_auth()

  email = web.find_element(By.ID, "ap_email")
  email.send_keys(user_login[0])

  password = web.find_element(By.ID, "ap_password")
  password.send_keys(user_login[1])

  sign_in_btn = web.find_element(By.ID, "signInSubmit")
  sign_in_btn.click()

def fetch_books(web):
  books = web.find_elements(By.CSS_SELECTOR, "h2.kp-notebook-searchable")
  for book in books:

    print(book, book.text.strip())

  print(f"No. of boooks: {len(books)}")


def main():
  browser = webdriver.Firefox()
  browser.get("https://read.amazon.com/kp/notebook")

  login(browser)
  fetch_books(browser)


if __name__ == "__main__":
  main()
