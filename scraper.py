#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getpass import getpass

def user_auth():
  email = input("Enter Amazon Email: ")
  password = getpass("Password: ")
  return (email, password)

def login(web):
  user_login = user_auth()

  email = web.find_element(By.ID, "ap_email")
  email.send_keys(user_login[0])

  password = web.find_element(By.ID, "ap_password")
  password.send_keys(user_login[1])

  sign_in_btn = web.find_element(By.ID, "signInSubmit")
  sign_in_btn.click()

def main():
  browser = webdriver.Firefox()
  browser.get("https://read.amazon.com/kp/notebook")

  login(browser)

if __name__ == "__main__":
  main()