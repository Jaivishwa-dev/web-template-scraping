import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()  # Track visited URLs to avoid duplicates

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def save_file(url, folder):
    """Downloads a file and saves it to the specified folder."""
    try:
        os.makedirs(folder, exist_ok=True)
        file_name = os.path.basename(urlparse(url).path) or "index.html"
        file_path = os.path.join(folder, file_name)

        response = requests.get(url, stream=True, headers=HEADERS)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Failed to download: {url} (Status code: {response.status_code})")
    except Exception as e:
        print(f"Error saving file {url}: {e}")

def scrape_page(url, base_url, output_folder):
    """Scrapes a single page and its assets."""
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Save the main HTML file
        relative_path = urlparse(url).path.lstrip("/").replace("/", "_") or "index.html"
        page_folder = os.path.join(output_folder, os.path.dirname(relative_path))
        os.makedirs(page_folder, exist_ok=True)
        with open(os.path.join(page_folder, os.path.basename(relative_path)), "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        # Static folder definitions
        static_folders = {
            "css": os.path.join(output_folder, "static", "css"),
            "js": os.path.join(output_folder, "static", "js"),
            "images": os.path.join(output_folder, "static", "images"),
            "fonts": os.path.join(output_folder, "static", "fonts"),
        }

        # Download assets (CSS, JS, Images, Fonts)
        for tag, attr, folder_key in [
            ("link", "href", "css"),
            ("script", "src", "js"),
            ("img", "src", "images"),
            ("source", "src", "images"),
        ]:
            for element in soup.find_all(tag):
                asset_url = element.get(attr)
                if asset_url:
                    full_url = urljoin(url, asset_url)
                    save_file(full_url, static_folders[folder_key])

        # Recursively scrape internal links
        for a_tag in soup.find_all("a", href=True):
            link = a_tag["href"]
            full_url = urljoin(base_url, link)

            # Only follow internal links (within the same domain)
            if urlparse(base_url).netloc == urlparse(full_url).netloc:
                scrape_page(full_url, base_url, output_folder)

    except requests.RequestException as e:
        print(f"Error scraping page {url}: {e}")

def scrape_website(base_url, output_folder):
    """Scrapes the entire website, including all pages and assets."""
    try:
        scrape_page(base_url, base_url, output_folder)
        print(f"Website scraping completed. Files saved in: {output_folder}")
    except Exception as e:

        print(f"Error scraping website: {e}")

if __name__ == "__main__":
    website_url = input("Enter the website URL: ").strip()
    folder_name = urlparse(website_url).netloc.replace(".", "_")
    scrape_website(website_url, folder_name)