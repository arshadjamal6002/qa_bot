# import requests
# from bs4 import BeautifulSoup
# import os
# import time

# # Final, comprehensive list based on site navigation
# URLS = [
#     # Main
#     'https://jupiter.money/',
#     'https://jupiter.money/contact/',
#     # Company
#     'https://jupiter.money/about-us/',
#     'https://jupiter.money/careers/',
#     'https://jupiter.money/product-roadmap/',
#     'https://jupiter.money/life-at-jupiter/',
#     # Accopunts
#     'https://jupiter.money/savings-account',
#     'https://jupiter.money/pro-salary-account/',
#     'https://jupiter.money/corporate-salary-account/',
#     'https://jupiter.money/pots/',

#     'https://jupiter.money/rewards/',

#     # Loans
#     'https://jupiter.money/loans/',
#     'https://jupiter.money/loan-against-mutual-funds/',

#     # Investments
#     'https://jupiter.money/investments/',
#     'https://jupiter.money/mutual-funds/',
#     'https://jupiter.money/digi-gold/',
#     'https://jupiter.money/flexi-fd/',
#     'https://jupiter.money/recurring-deposits/',
#     'https://jupiter.money/magic-spends/',

#     # Credit cards
#     'https://jupiter.money/edge-plus-upi-rupay-credit-card/',
#     'https://jupiter.money/edge-csb-rupay-credit-card/',
#     'https://jupiter.money/edge-visa-credit-card/',
#     # Resources
#     'https://jupiter.money/resources/blog/',
#     'https://jupiter.money/resources/calculators/',
#     # Legal & Useful Links
#     'https://jupiter.money/legal/pricing-and-fees/',
#     'https://jupiter.money/legal/terms-and-conditions/',
#     'https://jupiter.money/legal/privacy-policy/',
#     'https://jupiter.money/legal/grievance-redressal-policy/',
#     'https://jupiter.money/legal/communication-guidelines/',
# ]






import requests
from bs4 import BeautifulSoup
import os
import time

URL_LIST_FILE = "discovered_urls.txt" 
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "scraped_data.txt")

def load_urls_from_file(filepath):
    """Loads a list of URLs from a text file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Error: The file {filepath} was not found.")
        print("Please run the crawler.py script first to generate the list of URLs.")
        return []

def scrape_and_save():
    """Scrapes text from a list of URLs (from a file) and saves it."""
    urls = load_urls_from_file(URL_LIST_FILE)
    if not urls:
        return 
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("") 

    print(f"🚀 Starting scraper for {len(urls)} discovered links...")

    for url in urls:
        try:
            print(f"Scraping {url}...")
            response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)

            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n\n--- Content from {url} ---\n\n")
                f.write(text)
            
            time.sleep(1)

        except requests.RequestException as e:
            print(f"⚠️  Skipping {url}: {e}")

    print(f"\n✅ Scraping complete! Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_and_save()












# OUTPUT_DIR = "data"
# OUTPUT_FILE = os.path.join(OUTPUT_DIR, "scraped_data.txt")

# def scrape_and_save():
#     """Scrapes text from a list of URLs and saves it to a single text file."""
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)
    
#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         f.write("") # Clear the file

#     print("🚀 Starting definitive scraper...")

#     for url in URLS:
#         try:
#             print(f"Scraping {url}...")
#             response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
#             response.raise_for_status()

#             soup = BeautifulSoup(response.content, 'html.parser')
#             text = soup.get_text(separator=' ', strip=True)

#             with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
#                 f.write(f"\n\n--- Content from {url} ---\n\n")
#                 f.write(text)
            
#             time.sleep(1)

#         except requests.RequestException as e:
#             print(f"❌ Error scraping {url}: {e}")

#     print(f"✅ Definitive scraping complete! Data saved to {OUTPUT_FILE}")

# if __name__ == "__main__":
#     scrape_and_save()

