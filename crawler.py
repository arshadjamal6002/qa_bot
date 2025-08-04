import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time
import os

# The starting point for our crawl
START_URL = "https://jupiter.money/"
# The exact domain we want to stay on
ALLOWED_DOMAIN = "jupiter.money"
# File to save the discovered links
OUTPUT_FILE = "discovered_urls.txt"

def clean_url(url):
    """
    Cleans a URL by removing query parameters, fragments, and trailing slashes.
    """
    parsed = urlparse(url)
    clean_parsed = parsed._replace(params='', query='', fragment='')
    clean_url = urlunparse(clean_parsed)
    return clean_url.rstrip('/')

def crawl_site(start_url):
    """
    Crawls a website, discovering all unique, valid links on the EXACT specified
    domain, EXCLUDING blog sections.
    """
    urls_to_visit = {clean_url(start_url)}
    visited_urls = set()

    print(f"🚀 Starting restricted crawl from {start_url} (excluding blogs)...")

    while urls_to_visit:
        url = urls_to_visit.pop()
        if url in visited_urls:
            continue

        print(f"🔗 Visiting: {url}")
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(start_url, link['href'])
                cleaned_new_link = clean_url(absolute_link)
                
                # --- Stricter filtering logic ---
                if (urlparse(cleaned_new_link).netloc == ALLOWED_DOMAIN and
                        '/blog' not in cleaned_new_link and # --- NEW: Exclude blog URLs ---
                        cleaned_new_link not in visited_urls and
                        cleaned_new_link not in urls_to_visit and
                        urlparse(cleaned_new_link).scheme in ['http', 'https' ]):
                    
                    urls_to_visit.add(cleaned_new_link)

            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"❌ Could not fetch {url}: {e}")

    return sorted(list(visited_urls))

# --- Main execution ---
if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"Removed old '{OUTPUT_FILE}'.")

    final_links = crawl_site(START_URL)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in final_links:
            f.write(link + "\n")
            
    print(f"\n✅ Restricted crawl complete! Found {len(final_links)} non-blog links.")
    print(f"All valid links have been saved to {OUTPUT_FILE}")