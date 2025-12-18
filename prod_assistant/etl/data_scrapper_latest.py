import csv
import time
import re
import os
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class FlipkartScraper:
    def __init__(self, output_dir="data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_top_reviews(self, product_url, count=2):
        print(f"Fetching reviews for: {product_url}")
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = uc.Chrome(options=options, use_subprocess=True)

        if not product_url.startswith("http"):
            print("Invalid URL format.")
            driver.quit()
            return "No reviews found"

        try:
            driver.get(product_url)
            time.sleep(4)
            try:
                # Using ESCAPE as it's more reliable than finding the '✕' button
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                print("Attempted to close popup via Escape key")
            except Exception as e:
                print(f"Error occurred while closing popup: {e}")

            for _ in range(4):
                ActionChains(driver).send_keys(Keys.END).perform()
                time.sleep(1.5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # UPDATED: Common classes for review blocks across different layouts
            review_blocks = soup.select("div.EPCmJX, div.RC_N1D, div._27M-vq")
            print(f"Found {len(review_blocks)} potential review blocks")

            seen = set()
            reviews = []

            for block in review_blocks:
                # UPDATED: Common classes for the actual text body
                text_el = block.select_one("div.ZmyHeS, div.t-ZTKy, div._6K-7Co")
                if text_el:
                    text = text_el.get_text(separator=" ", strip=True)
                    if text and text not in seen:
                        reviews.append(text)
                        seen.add(text)
                if len(reviews) >= count:
                    break
        except Exception as e:
            print(f"General Exception in get_top_reviews: {e}")
            reviews = []
            
        print("Final reviews found:", reviews)
        driver.quit()
        return " || ".join(reviews) if reviews else "No reviews found"
    
    def scrape_flipkart_products(self, query, max_products=1, review_count=2):
        print(f"Searching for: {query}")
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options, use_subprocess=True)
        search_url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
        driver.get(search_url)
        time.sleep(4)

        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        except Exception as e:
            print(f"Error occurred while closing search popup: {e}")

        time.sleep(2)
        products = []

        # UPDATED: Common containers for both List and Grid views
        items = driver.find_elements(By.CSS_SELECTOR, "div.CGtC98, div._75_9_G, div[data-id]")[:max_products]
        print(f"Found {len(items)} items on search page")

        for item in items:
            try:
                # UPDATED: Multi-selector approach for higher success rate
                title = item.find_element(By.CSS_SELECTOR, "div.KzDlHZ, a.w1Y96d, div._W9uB7").text.strip()
                price = item.find_element(By.CSS_SELECTOR, "div.Nx9bqj, div._1+u29z").text.strip()
                
                # Handling ratings that might be missing
                try:
                    rating = item.find_element(By.CSS_SELECTOR, "div.XQDdHH, div._3LWZlK").text.strip()
                except:
                    rating = "N/A"
                
                try:
                    reviews_text = item.find_element(By.CSS_SELECTOR, "span.Wphh3N, span._2_R_oP").text.strip()
                    match = re.search(r"([\d,]+)", reviews_text)
                    total_reviews = match.group(1) if match else "N/A"
                except:
                    total_reviews = "0"

                link_el = item.find_element(By.CSS_SELECTOR, "a[href*='/p/']")
                href = link_el.get_attribute("href")
                product_link = href if href.startswith("http") else "https://www.flipkart.com" + href
                
                match_id = re.search(r"/p/(itm[0-9A-Za-z]+)", href)
                product_id = match_id.group(1) if match_id else "N/A"

                print(f"Processing product: {title[:30]}...")
                top_reviews = self.get_top_reviews(product_link, count=review_count)
                
                products.append([product_id, title, rating, total_reviews, price, top_reviews])

            except Exception as e:
                print(f"Error occurred while processing item: {e}")
                continue

        driver.quit()
        return products

    def save_to_csv(self, data, filename="product_reviews.csv"):
        path = os.path.join(self.output_dir, filename)
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["product_id", "product_title", "rating", "total_reviews", "price", "top_reviews"])
                writer.writerows(data)
            print(f"Successfully saved data to {path}")
        except Exception as e:
            print(f"Error saving CSV: {e}")