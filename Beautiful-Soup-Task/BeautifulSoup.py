from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

class Logger:
    @staticmethod
    def setup():
        logging.basicConfig(
            filename="dell_scrape_results.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

class DellScraper:
    def __init__(self, url):
        self.url = url
        self.base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))
        self.html = None
        Logger.setup()

    def fetch_page(self):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url, timeout=60000)
                page.wait_for_load_state("networkidle")
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.html = page.content()
                browser.close()
        except PlaywrightTimeoutError:
            logging.error(f"Timeout while loading {self.url}")
        except Exception as e:
            logging.error(f"Error fetching {self.url}: {e}")

    def parse_elements(self):
        if not self.html:
            logging.error("No HTML content to parse.")
            return

        soup = BeautifulSoup(self.html, "html.parser")

        #Extracting images
        images = soup.find_all("img")
        for img in images:
            src = img.get("src")
            src = urljoin(self.base_url, src) if src else "No Source"
            alt = img.get("alt", "No Alt Text")
            logging.info(f"Image - Source: {urljoin(self.base_url, src)}, Alt: {alt}")

        # Extracting hyperlinks
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            href = urljoin(self.base_url, href) if href and href.startswith("/") else href or "No URL"
            text = link.get_text(strip=True) or "No Text"
            logging.info(f"Hyperlink - Text: {text}, URL: {href}")

        # Extracting buttons
        buttons = soup.find_all("button")
        for button in buttons:
            button_text = button.get_text(" ",strip=True) or "No Text"
            logging.info(f"Button - Text: {button_text}")

        print("Scraping completed successfully!")

    def run(self):
        print(f"Starting scraper for {self.url}")
        self.fetch_page()
        self.parse_elements()


if __name__ == "__main__":
    dell_scraper = DellScraper("https://www.dell.com/support/home/en-us")
    dell_scraper.run()
