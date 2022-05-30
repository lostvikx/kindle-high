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
from time import sleep


def fetch_highlights_to_del(web):
  
  highlight_divs = web.find_elements(By.CSS_SELECTOR, ".a-row.a-spacing-base > .a-column.a-span10.kp-notebook-row-separator")

  highlights_to_del = []

  for div in highlight_divs:
    highlight = div.find_element(By.ID, "highlight").text.strip()

    if len(highlight.split()) <= 3:
      highlights_to_del.append(div)

  return highlights_to_del


def fetch_highlight_to_del(web):

  highlight_divs = web.find_elements(By.CSS_SELECTOR, ".a-row.a-spacing-base > .a-column.a-span10.kp-notebook-row-separator")

  for high_div in highlight_divs:
    highlight = high_div.find_element(By.ID, "highlight").text.strip()
    if len(highlight.split()) <= 3:
      return high_div
    else:
      continue

  return None


def wait_until_clickable(web, element, delay):
  try:
    loaded_element = WebDriverWait(web, delay).until(EC.element_to_be_clickable(element))
    complete_load = WebDriverWait(web, delay).until(EC.visibility_of(loaded_element))
  except TimeoutError:
    print("Element couldn't be clickable!")
  except Exception as err:
    print(f"Something went wrong: {err}")

  return complete_load


def click_element(web, element):
  webdriver.ActionChains(web).move_to_element(element).click(element).perform()


def delete_highlight(web, highlight_div):
  delay = 100

  options_btn = highlight_div.find_element(By.CSS_SELECTOR, "a.a-popover-trigger.a-declarative")
  options_btn_ready = wait_until_clickable(web, options_btn, delay)
  click_element(web, options_btn_ready)

  delete_btn = web.find_element(By.ID, "deletehighlight")
  delete_btn_ready = wait_until_clickable(web, delete_btn, delay)
  click_element(web, delete_btn_ready)

  delete_confirm_btn = web.find_element(By.ID, "deleteHighlight")
  delete_confirm_btn_ready = wait_until_clickable(web, delete_confirm_btn, delay)
  click_element(web, delete_confirm_btn_ready)

  # this is a quick fix
  sleep(5)


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

  while True:
    high_div = fetch_highlight_to_del(browser)

    if high_div != None:
      delete_highlight(browser, high_div)
      continue
    else:
      print("Everything looks good!")
      break

  browser.close()
  print("Useless highlights were deleted!")

  # for index, book in enumerate(books):
  #   is_first = False
  #   if index == 0:
  #     is_first = True

  #   wait_payload(browser, book, is_first, 100)
  #   highs = fetch_highlights_to_del(browser)

if __name__ == "__main__":
  main()
