import os
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

        # Define the templates folder
        templates_folder = os.path.join(output_folder, "templates")
        os.makedirs(templates_folder, exist_ok=True)

        # Save the main HTML file in the templates folder
        relative_path = urlparse(url).path.lstrip("/").replace("/", "_") or "index.html"
        html_file_path = os.path.join(templates_folder, os.path.basename(relative_path))

        # Static folder definitions
        static_folders = {
            "css": os.path.join(output_folder, "static", "css"),
            "js": os.path.join(output_folder, "static", "js"),
            "images": os.path.join(output_folder, "static", "images"),
            "fonts": os.path.join(output_folder, "static", "fonts"),
        }

        # Fix asset paths in HTML
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
                    asset_file_name = os.path.basename(urlparse(full_url).path)
                    new_path = f"../static/{folder_key}/{asset_file_name}"
                    element[attr] = new_path  # Update path in HTML
                    save_file(full_url, static_folders[folder_key])

        # Save the modified HTML
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print(f"Saved HTML: {html_file_path}")

        # Recursively scrape internal links
        for a_tag in soup.find_all("a", href=True):
            link = a_tag["href"]
            full_url = urljoin(base_url, link)

            # Only follow internal links (within the same domain)
            if urlparse(base_url).netloc == urlparse(full_url).netloc:
                scrape_page(full_url, base_url, output_folder)

    except requests.RequestException as e:
        print(f"Error scraping page {url}: {e}")


def scrape_website(base_url):
    """Scrapes the entire website, including all pages and assets."""
    folder_name = input("Enter the folder name to save the website: ").strip()

    if not folder_name:
        print("Invalid folder name! Using default domain-based name.")
        folder_name = urlparse(base_url).netloc.replace(".", "_")

    output_folder = os.path.join(os.getcwd(), folder_name)

    try:
        scrape_page(base_url, base_url, output_folder)
        print(f"Website scraping completed. Files saved in: {output_folder}")
    except Exception as e:
        print(f"Error scraping website: {e}")


if __name__ == "__main__":
    website_url = input("Enter the website URL: ").strip()
    scrape_website(website_url)
