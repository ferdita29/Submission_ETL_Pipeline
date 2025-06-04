import time
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

BASE_URL = "https://fashion-studio.dicoding.dev/"
MAX_PAGES = 50
TARGET_DATA = 1000

def fetch_page_data(url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Terjadi kesalahan saat mengambil {url}: {e}")
        return None

def extract_product_data(product_element) -> dict:
    try:
        title = product_element.find("h3", class_="product-title").text.strip()
        price = product_element.find("span", class_="price").text.strip().replace("$", "")
        rating_text = product_element.find_all("p")[0].text
        rating = rating_text.strip().split(" ")[-3]

        details = [p.text.strip() for p in product_element.find_all("p")[1:]]
        colors = details[0].split()[0]
        size = details[1].replace("Size:", "").strip()
        gender = details[2].replace("Gender:", "").strip()

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        }
    except (AttributeError, IndexError) as e:
        print(f"Data produk tidak lengkap atau rusak: {e}")
        return {}

def scrape_page_data(url: str) -> list:
    soup = fetch_page_data(url)
    if not soup:
        return []
    products = []
    product_elements = soup.find_all("div", class_="collection-card")
    for product in product_elements:
        product_data = extract_product_data(product)
        if product_data:
            products.append(product_data)
    return products

def scrape_all_pages(start_page=1, end_page=MAX_PAGES) -> list:
    all_products = []
    seen_titles = set()
    for page in range(start_page, end_page + 1):
        print(f"Scraping halaman {page}...")
        url = BASE_URL if page == 1 else f"{BASE_URL}page{page}"
        try:
            page_products = scrape_page_data(url)
            print(f"Ditemukan {len(page_products)} produk di halaman {page}")
            for product in page_products:
                if product["Title"] not in seen_titles:
                    seen_titles.add(product["Title"])
                    all_products.append(product)
            if len(all_products) >= TARGET_DATA:
                print(f"Sudah mencapai target data: {TARGET_DATA} produk.")
                break
            time.sleep(2)
        except Exception as e:
            print(f"Terjadi kesalahan saat scraping halaman {page}: {e}")
    return all_products

if __name__ == "__main__":
    products = scrape_all_pages()
    df = pd.DataFrame(products)
    df.to_csv("scraped_products.csv", index=False)
    print("Data berhasil disimpan ke scraped_products.csv.")
