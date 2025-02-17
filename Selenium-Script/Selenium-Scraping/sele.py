import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class PageElementExtractor:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def _setup_driver(self):
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logging.error(f"Error setting up the driver: {e}")
            self.driver = None

    def _wait_for_page_load(self):
        if self.driver:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def _log_images(self):
        if self.driver:
            images = self.driver.find_elements(By.TAG_NAME, "img")
            for img in images:
                src = img.get_attribute("src")
                alt = img.get_attribute("alt")
                logging.info(f"Image Source: {src}, Alt Text: {alt}")

    def _log_links(self):
        if self.driver:
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href") or "No URL"
            
                text = (link.get_attribute("innerText") or link.text or "Icon found").strip()
                logging.info(f"Link Text: {text}, URL: {href}")

            if not text:
                for child in link.find_elements(By.XPATH, ".//*"):
                    child_text = (child.get_attribute("innerText") or child.text or "").strip()
                    if child_text:
                        break

                    logging.info(f"Link Text: {text}, URL: {href}")


    def _log_buttons(self):
        if self.driver:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            button_text = (button.get_attribute("innerText") or button.text or "").strip()
            logging.info(f"Button: {button_text}")

            if button_text == '':
                icon_element = button.find_elements(By.XPATH, ".//i | .//svg")  # Look for <i> or <svg> (commonly used for icons)
                if icon_element:
                    icon_html = icon_element[0].get_attribute("outerHTML")
                    button_text = f"Icon Button: {icon_html}"
                else:
                    button_text = "No Text"

            logging.info(f"Button: {button_text}")


    def extract_elements(self):
        try:
            self._setup_driver()
            if self.driver:
                self.driver.get(self.url)
                self._wait_for_page_load()
                logging.info(f"Extracting elements from: {self.url}")
                self._log_images()
                self._log_links()
                self._log_buttons()
            else:
                logging.error("Driver was not initialized correctly.")
        except Exception as e:
            logging.error(f"An error occurred during extraction: {e}")
        finally:
            if self.driver:
                self.driver.quit()

def setup_logging():
    logging.basicConfig(filename="page_elements.log", level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    setup_logging()
    url = "https://www.dell.com/support/home/en-us"
    extractor = PageElementExtractor(url)
    extractor.extract_elements()
    print("Element extraction completed successfully.")

if __name__ == "__main__":
    main()
