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


def fetch_highlights_to_del(web):
  
  highlight_divs = web.find_elements(By.CSS_SELECTOR, ".a-row.a-spacing-base > .a-column.a-span10.kp-notebook-row-separator")

  highlights_to_del = []

  for div in highlight_divs:
    highlight = div.find_element(By.ID, "highlight").text.strip()

    if len(highlight.split()) <= 3:
      highlights_to_del.append(div)

  return highlights_to_del


def wait_until_clickable(web, element, delay):
  try:
    loaded_element = WebDriverWait(web, delay).until(EC.element_to_be_clickable(element))
    complete_load = WebDriverWait(web, delay).until(EC.visibility_of(loaded_element))
  except TimeoutError:
    print("Element couldn't be clickable!")
  except Exception as err:
    print(f"Something went wrong: {err}")

  return complete_load


def delete_highlights(web, highlight_divs):

  delay = 100
  
  for div in highlight_divs:
    options_btn = div.find_element(By.CSS_SELECTOR, "a.a-popover-trigger.a-declarative")
    options_btn_ready = wait_until_clickable(web, options_btn, delay)
    webdriver.ActionChains(web).move_to_element(options_btn_ready).click(options_btn_ready).perform()

    delete_btn = web.find_element(By.ID, "deletehighlight")
    delete_btn_ready = wait_until_clickable(web, delete_btn, delay)
    webdriver.ActionChains(web).move_to_element(delete_btn_ready).click(delete_btn_ready).perform()

    delete_confirm_btn = web.find_element(By.ID, "deleteHighlight")
    delete_confirm_btn_ready = wait_until_clickable(web, delete_confirm_btn, delay)
    webdriver.ActionChains(web).move_to_element(delete_confirm_btn_ready).click(delete_confirm_btn_ready).perform()
    # web.execute_script("arguments[0].click();", delete_it)


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

  # test
  wait_payload(browser, books[26], False, 100)
  highlights_to_del = fetch_highlights_to_del(browser)
  # browser.maximize_window()
  delete_highlights(browser, highlights_to_del)

  browser.close()
  print("Useless highlights were deleted!")

  # for index, book in enumerate(books):
  #   is_first = False
  #   if index == 0:
  #     is_first = True

  #   # [atleast 1 highlight in the list]
  #   wait_payload(browser, book, is_first, 100)
  #   highs = fetch_highlights_to_del(browser)

if __name__ == "__main__":
  main()
