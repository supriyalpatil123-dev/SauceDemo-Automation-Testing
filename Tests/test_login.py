
import pytest
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Pages.LoginPage import LoginPage

# Read login credentials from JSON file
json_file_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Fixtures",
    "Data.json"
)

with open(json_file_path, "r") as json_file:
    Data = json.load(json_file)

username = Data["credentials"]["username"]
password = Data["credentials"]["password"]
url = Data["URL"]


@pytest.fixture(scope="module")
def driver():
    # Open Chrome browser
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    # Keep browser open until you close it manually
    print("\nTests finished!")
    print("Close the Chrome window using the X button.")

    try:
        while True:
            try:
                # Check whether the browser is still open
                driver.current_window_handle
            except Exception:
                break

            time.sleep(1)
    finally:
        driver.quit()


# Test login with valid credentials
def test_valid_login(driver):
    login_page = LoginPage(driver)

    driver.get(url)

    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    # Verify successful login
    assert "inventory.html" in driver.current_url, \
        "Valid login failed!"


# Test login with invalid credentials
def test_invalid_login(driver):
    login_page = LoginPage(driver)

    driver.get("https://www.saucedemo.com/")

    login_page.enter_username(username)
    login_page.enter_password("wrong-password")
    login_page.click_login()

    # Verify error message appears
    error_message = driver.find_element(
        By.CSS_SELECTOR, '[data-test="error"]'
    )

    assert error_message.is_displayed(), \
        "Invalid login error message not displayed!"
