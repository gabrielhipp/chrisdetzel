from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import re

def scrape_holzprofi_product(driver):
    wait = WebDriverWait(driver, 5)

    def reject_cookies_if_present(driver):
        try:
            reject_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@class='rhc-banner__content__secondary']")
                )
            )
            reject_button.click()
            reject_button2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@class='rhc-settings__content__footer__secondary']")
                )
            )
            reject_button2.click()
            # Kurze Wartezeit, damit Overlay verschwindet
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element(reject_button2)
            )
            return True
        except TimeoutException:
            # Cookie Banner nicht vorhanden → ok
            return False

    def extract_price_and_stock(text):
        # Normalisiere whitespace
        txt = text.strip()
        
        # 1) Preis finden (Versuche zuerst mit Euro-Zeichen, dann generisch)
        price_patterns = [
            r'€\s*([0-9][0-9\.,\s]*)',                 # z.B. "€ 439,00"
            r'Preis[:\s]*([0-9][0-9\.,\s]*)',          # z.B. "Preis: 439,00"
            r'([0-9]+[.,][0-9]{2})'                    # z.B. "439,00" (Fallback)
        ]
        price_raw = None
        price_value = None
        for p in price_patterns:
            m = re.search(p, txt, flags=re.IGNORECASE)
            if m:
                price_raw = m.group(1).strip()
                break

        if price_raw:
            # Entferne geschützte Leerzeichen, normalize spaces
            s = price_raw.replace('\xa0', '').replace(' ', '')
            # Fälle unterscheiden:
            # - Wenn sowohl '.' als auch ',' vorkommen: '.' = Tausender, ',' = Dezimal
            if '.' in s and ',' in s:
                s_norm = s.replace('.', '').replace(',', '.')
            else:
                # nur ',' vorhanden -> Komma als Dezimaltrenner
                if ',' in s and '.' not in s:
                    s_norm = s.replace(',', '.')
                # nur '.' vorhanden -> wenn genau 2 Nachkommastellen -> handelt sich um Dezimalpunkt, sonst Tausender
                elif '.' in s and len(s.split('.')[-1]) == 2:
                    s_norm = s  # bleibt so, float() kann das ggf. nicht direkt (setzt Punkt voraus)
                else:
                    s_norm = s.replace('.', '')
            # Letzte Sicherung: wenn noch Komma da ist, ersetze durch Punkt
            s_norm = s_norm.replace(',', '.')
            try:
                price_value = float(s_norm)
            except ValueError:
                price_value = None

        # 2) Lagerstatus finden (häufige Ausdrücke)
        stock_keywords = [
            r'AUF\s+LAGER',
            r'SOFORT\s+LIEFERBAR',
            r'LIEFERBAR',
            r'AUSVERKAUFT',
            r'NICHT\s+LIEFERBAR',
            r'VORBESTELLBAR',
            r'IN\s+WAREN[Kk]ORB',   # manchmal "IN WARENKORB" anzeigen
            r'ANFRAGE\s+SENDEN'     # z.B. statt sofort kaufbar
        ]
        stock_pattern = re.compile(r'(' + '|'.join(stock_keywords) + r')', flags=re.IGNORECASE)
        stock_match = stock_pattern.search(txt)
        stock_raw = stock_match.group(1).upper() if stock_match else None

        # Vereinheitlichte Statusnamen (optional)
        status_mapping = {
            'AUF LAGER': 'auf lager',
            'SOFORT LIEFERBAR': 'auf lager',
            'LIEFERBAR': 'auf lager',
            'AUSVERKAUFT': 'ausverkauft',
            'NICHT LIEFERBAR': 'nicht lieferbar',
            'VORBESTELLBAR': 'vorbestellbar',
            'IN WARENKORB': 'in warenkorb',
            'ANFRAGE SENDEN': 'anfrage senden'
        }
        stock_normalized = None
        if stock_raw:
            # nimm den exakten Schlüssel (ohne extra spaces)
            key = re.sub(r'\s+', ' ', stock_raw).strip()
            stock_normalized = status_mapping.get(key, key.lower())

        return {
            'price_raw': price_raw,           # z.B. "439,00" oder "€ 439,00" (ohne davor bei unseren patterns)
            'price_value': price_value,       # float (z.B. 439.0) oder None
            'stock_raw': stock_raw,           # gefundenes Original (groß)
            'stock_normalized': stock_normalized  # vereinheitlicht (klein)
        }

    # Beispiel:
    #combined_text = "Preis: € 439,00\nAUF LAGER\n+ inkl. USt., exkl. Versandkosten\n-\n+\nIN WARENKORB\nANFRAGE SENDEN"
    #print(extract_price_and_stock(combined_text))
    
    reject_cookies_if_present(driver)

    combined_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@class='mt-12 grid items-stretch']")
        )
    )

    combined_text = combined_element.text.strip()

    json_of_combined_section = extract_price_and_stock(combined_text)
    price_number = int(float(json_of_combined_section['price_raw'].replace('€', '').strip().replace('.', '').replace(',', '.')))
    print(f"Price: {price_number}")
    print(f"Stock: {json_of_combined_section['stock_raw']}")
    
    return {
        "price": price_number,
        "availability": json_of_combined_section["stock_raw"],
        "shipping_costs": "-",
    }