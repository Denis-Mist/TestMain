"""Экспорт сценария входа (ПР14) в pytest + Selenium WebDriver."""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    yield browser
    browser.quit()


@pytest.mark.parametrize(
    "username,password,expect_inventory",
    [
        ("standard_user", "secret_sauce", True),
        ("locked_out_user", "secret_sauce", False),
    ],
)
def test_saucedemo_login(driver, username, password, expect_inventory):
    driver.get("https://www.saucedemo.com/")
    assert "Swag Labs" in driver.title

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 10)
    if expect_inventory:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".inventory_list")))
        assert driver.find_element(By.CSS_SELECTOR, ".title").text == "Products"
    else:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        assert "locked out" in driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text.lower()
