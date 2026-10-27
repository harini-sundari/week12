
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


URL = "http://127.0.0.1:5002/"


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    yield driver
    driver.quit()


def submit_form(driver, username, password):
    driver.get(URL)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "pwd").send_keys(password)
    driver.find_element(By.NAME, "sb").click()


def read_alert(driver):
    alert = WebDriverWait(driver, 5).until(
        lambda d: d.switch_to.alert
    )
    message = alert.text
    alert.accept()
    return message


def test_empty_username(setup_teardown):
    driver = setup_teardown
    submit_form(driver, "", "Password123")
    assert read_alert(driver) == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    submit_form(driver, "John Doe", "")
    assert read_alert(driver) == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    submit_form(driver, "Jane", "abc1")
    assert read_alert(driver) == (
        "Password must be at least 6 characters long."
    )


def test_valid_input(setup_teardown):
    driver = setup_teardown
    submit_form(driver, "Alice", "abc123")

    WebDriverWait(driver, 10).until(
        lambda d: "/submit" in d.current_url
    )

    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Hello, Alice! Welcome to the website" in body_text
