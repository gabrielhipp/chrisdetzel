from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def scrape_neureiter_product(driver):
    
    wait = WebDriverWait(driver, 3)

    price_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@class='price']")
        )
    )
    price_text = price_element.text.strip()
    price_number = int(float(price_text.replace('€', '').strip().replace('.', '').replace(',', '.')))
    print(f"Price: {price_number}")

    
    stock_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@class='stock-info']")
        )
    )
    stock_text = stock_element.text.strip()
    print(f"Stock: {stock_text}")
    return {
        "price": price_number,
        "availability": stock_text,
        "shipping_costs": "-",
    }