import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# The starting point for our crawl
START_URL = "https://jupiter.money/"
# The domain we want to stay within
DOMAIN = "jupiter.money"
# File to save the discovered links
OUTPUT_FILE = "discovered_urls.txt"

def crawl_site(start_url):
    """
    Crawls a website starting from start_url, discovering all unique, valid links
    within the same domain.
    """
    urls_to_visit = {start_url}
    visited_urls = set()
    discovered_links = set()

    print(f"🚀 Starting crawl from {start_url}...")

    while urls_to_visit:
        url = urls_to_visit.pop()
        if url in visited_urls:
            continue

        print(f"🔗 Visiting: {url}")
        visited_urls.add(url)
        # Add the valid URL to our final list
        discovered_links.add(url)

        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                # Join relative URLs (e.g., '/about-us') with the base URL
                absolute_link = urljoin(start_url, href)
                
                # --- Filtering Logic ---
                # 1. Check if it's within the same domain
                # 2. Check if it's not already visited
                # 3. Check if it's a web page (not a file or mailto link)
                if (DOMAIN in urlparse(absolute_link).netloc and
                        absolute_link not in visited_urls and
                        absolute_link not in urls_to_visit and
                        '#' not in absolute_link and # Exclude page anchors
                        not absolute_link.endswith(('.pdf', '.jpg', '.png', '.zip')) and
                        not absolute_link.startswith('mailto:')):
                    
                    urls_to_visit.add(absolute_link)

            time.sleep(1) # Be respectful to the server

        except requests.RequestException as e:
            print(f"❌ Could not fetch {url}: {e}")

    return sorted(list(discovered_links))


# --- Main execution ---
if __name__ == "__main__":
    final_links = crawl_site(START_URL)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in final_links:
            f.write(link + "\n")
            
    print(f"\n✅ Crawl complete! Found {len(final_links)} unique links.")
    print(f"All valid links have been saved to {OUTPUT_FILE}")