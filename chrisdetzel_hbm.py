from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def scrape_hbm_product(driver):
    def reject_cookies_if_present(driver, timeout=5):
        try:
            wait = WebDriverWait(driver, timeout)
            reject_button = wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "onetrust-reject-all-handler")
                )
            )
            reject_button.click()
            # Kurze Wartezeit, damit Overlay verschwindet
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element(reject_button)
            )
            return True
        except TimeoutException:
            # Cookie Banner nicht vorhanden → ok
            return False

    reject_cookies_if_present(driver)


    wait = WebDriverWait(driver, 3)

    price_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@aria-label='Preis']")
        )
    )

    price_text = price_element.text.strip()
    price_number = int(float(price_text.replace('€', '').strip().replace('.', '').replace(',', '.')))
    print(f"Price: {price_number}")

    stock_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@class='text-sm']")
        )
    )
    stock_text = stock_element.text.strip()
    print(f"Stock: {stock_text}")
    return {
        "price": price_number,
        "availability": stock_text,
        "shipping_costs": "-",
    }