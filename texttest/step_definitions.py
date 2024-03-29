import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup(url):
    global driver, orig_url
    orig_url = url

    delay = float(os.getenv("USECASE_REPLAY_DELAY", "0"))
    options = webdriver.ChromeOptions()
    if delay:
        options.add_argument("--start-maximized")
    else:
        options.add_argument("--headless=new")

    options.set_capability('goog:loggingPrefs', {'browser':'ALL'})
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    print_html_page("start_page")


def print_html_page(page_name):
    html = driver.page_source
    with open(f"{page_name}.html", "w", encoding="utf-8") as f:
        f.write(html)


def wait_until(condition):
    try:
        return WebDriverWait(driver, 30).until(condition)
    except Exception as e:
        sys.stderr.write(f"Timed out {repr(driver)}\n")
        driver.quit()
        raise


def select_garden_size(size):
    garden_selector = Select(driver.find_element(By.ID, "select-garden-size"))
    garden_selector.select_by_visible_text(size)


def submit_garden_quizz():
    submit_button = driver.find_element(By.ID, "submit-garden-quizz")
    submit_button.click()


def select_flowers(flowers: list):
    for flower in flowers:
        checkbox_selector = driver.find_element(By.ID, f"label_{flower}")
        checkbox_selector.click()


def wait_for_garden_quizz_response():
    WebDriverWait(driver, 10).until_not(
        EC.text_to_be_present_in_element((By.ID, "garden_advice"), "Loading...")
    )


def enter_contact_details(name, email):
    name_field = driver.find_element(By.ID, "newsletter_name")
    name_field.send_keys(name)
    email_field = driver.find_element(By.ID, "newsletter_email")
    email_field.send_keys(email)

def submit_newsletter():
    submit_button = driver.find_element(By.ID, "newsletter_submit")
    submit_button.click()


def wait_for_newsletter_response():
    WebDriverWait(driver, 10).until_not(
        EC.text_to_be_present_in_element((By.ID, "newsletter_greeting"), "Loading...")
    )


def close():
    print_html_page("end_page")
    driver.quit()
