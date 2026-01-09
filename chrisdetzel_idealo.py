from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_idealo_product(driver):
    def reject_cookies_if_present(driver, timeout=5):
        try:
            time.sleep(1)
            
            # JavaScript to find and click the deny button inside shadow DOM
            script = """
            const shadowHost = document.querySelector('#usercentrics-cmp-ui');
            if (shadowHost && shadowHost.shadowRoot) {
                const denyButton = shadowHost.shadowRoot.querySelector('#deny');
                if (denyButton) {
                    denyButton.click();
                    return true;
                }
            }
            return false;
            """
            
            result = driver.execute_script(script)
            if result:
                print("Successfully clicked deny button in shadow DOM")
                time.sleep(1)
                return True
            else:
                print("Could not find deny button in shadow DOM")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    reject_cookies_if_present(driver)


    wait = WebDriverWait(driver, 3)

    """ listprice element """
    price_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@class='productOffers-listItemOfferPrice']")
        )
    )
    time.sleep(1)
    """ liststock element """
    stock_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@class='productOffers-listItemOfferDeliveryStatusDatesRange']")
        )
    )

    stock_text = stock_element.text.strip()
    price_text = price_element.text.strip()

    def parse_price(price_str):
        # Remove the € symbol and whitespace
        price_str = price_str.replace('€', '').strip()
        
        # Replace German number format: 3.890,00 → 3890.00
        # Remove thousands separator (.) and replace decimal separator (,) with (.)
        price_str = price_str.replace('.', '').replace(',', '.')
        
        # Convert to float, then to int if no decimals needed
        price_float = float(price_str)
        price_int = int(price_float)
        
        return price_int

    price_number = parse_price(price_text)
    print(f"Price number: {price_number}")
    print(f"Stock text: {stock_text}")

    return {
        "price": price_number,
        "availability": stock_text,
        "shipping_costs": "-",
    }