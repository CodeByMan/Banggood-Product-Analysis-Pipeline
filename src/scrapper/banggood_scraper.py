import os
import time
import random
import pandas as pd
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from util.file_paths import RAW_DATA_DIR
from util.logger import log


# -------- CONFIG --------
CATEGORIES = {
    "phones": "https://www.banggood.com/search/phones.html?from=nav&page={}",
    "smartwatches": "https://www.banggood.com/search/smartwatches.html?from=nav&page={}",
    "laptops": "https://www.banggood.com/search/laptops.html?from=nav&page={}",
    "rc_drones": "https://www.banggood.com/search/rc-drones.html?from=nav&page={}",
    "home_appliances": "https://www.banggood.com/search/home-appliances.html?from=nav&page={}"
}

os.makedirs(RAW_DATA_DIR, exist_ok=True)
MAX_PAGES = 5

# -------- Selenium driver --------
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# -------- Scraping logic --------
def scrape_category(category_name, url_template, max_pages=MAX_PAGES):
    driver = get_driver()
    all_products = []

    print(f"\nScraping category: {category_name}")

    for page in tqdm(range(1, max_pages + 1), desc=f"{category_name} pages"):
        url = url_template.format(page)
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        items = driver.find_elements(By.CSS_SELECTOR, "div.p-wrap")
        if not items:
            print(f"No items found on page {page}, stopping.")
            break

        for item in items:
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, "a.title")
                name = title_elem.text.strip()
                product_url = title_elem.get_attribute("href")
            except:
                name = None
                product_url = None

            try:
                price = item.find_element(By.CSS_SELECTOR, "span.price").text.strip()
            except:
                price = None

            try:
                old_price = item.find_element(By.CSS_SELECTOR, "span.price-old").text.strip()
            except:
                old_price = None

            try:
                discount = item.find_element(By.CSS_SELECTOR, "span.price-discount").text.strip()
            except:
                discount = None

            try:
                reviews = item.find_element(By.CSS_SELECTOR, "a.review").text.strip()
            except:
                reviews = None

            try:
                rating = item.find_element(By.CSS_SELECTOR, "span.review-text").text.strip()
            except:
                rating = None

            all_products.append({
                "category": category_name,
                "product_name": name,
                "product_url": product_url,
                "price": price,
                "old_price": old_price,
                "discount": discount,
                "reviews": reviews,
                "rating": rating
            })

        time.sleep(random.uniform(1.5, 3.0))

    driver.quit()

    df = pd.DataFrame(all_products)
    df.to_csv(os.path.join(RAW_DATA_DIR, f"{category_name}_raw.csv"), index=False)
    print(f"Saved {len(all_products)} items to {RAW_DATA_DIR}/{category_name}_raw.csv")

def main():
    for category, link in CATEGORIES.items():
        scrape_category(category, link)

if __name__ == "__main__":
    main()
