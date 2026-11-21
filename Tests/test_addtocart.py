
import pytest
import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.LoginPage import LoginPage
from Pages.Addtocart import Addtocart

# Read login credentials
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


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


def login(driver):
    login_page = LoginPage(driver)
    driver.get(url)

    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.ID, "inventory_container")
        )
    )


# TEST 1: Add products and complete checkout
def test_add_items_checkout(driver):
    login(driver)

    addtocart = Addtocart(driver)

    addtocart.add_items()
    addtocart.open_cart()

    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.ID, "checkout")
        )
    )

    addtocart.checkout()
    addtocart.assert_confirmation_message()
    addtocart.logout()


# TEST 2: Add and remove products
def test_add_remove_product(driver):
    login(driver)

    # Add backpack
    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()

    # Add bike light
    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-bike-light"
    ).click()

    # Verify cart contains 2 products
    badge = driver.find_element(
        By.CLASS_NAME, "shopping_cart_badge"
    )
    assert badge.text == "2"

    # Remove backpack
    driver.find_element(
        By.ID, "remove-sauce-labs-backpack"
    ).click()

    # Verify cart contains 1 product
    badge = driver.find_element(
        By.CLASS_NAME, "shopping_cart_badge"
    )
    assert badge.text == "1"

    print("Add and Remove Product Test Passed!")
