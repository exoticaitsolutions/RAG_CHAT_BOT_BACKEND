from urllib.parse import urljoin
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from seleniumbase import Driver
import time

# Set HEADLESS mode
HEADLESS = True

class SeleniumScraperServices:
    """
    Selenium-based web scraper service class.
    """
    
    @staticmethod
    def init_web_driver():
        """
        Initializes and returns a Selenium WebDriver instance.
        """
        try:
            options = {"uc": True, "headless": True}
            user_agent = UserAgent().random
            driver = Driver(**options)
            driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{get: function() {{ return '{user_agent}'; }} }});")
            return driver
        except Exception as e:
            print(f"An error occurred while initializing the web driver: {e}")
            return None
    
    @staticmethod
    def get_links_selenium(website_url):
        """
        Extracts all links from a given website URL.
        """
        try:
            driver = SeleniumScraperServices.init_web_driver()
            if not driver:
                return False, []
            
            print(f"Opening website: {website_url}")
            driver.get(website_url)
            time.sleep(3)
            
            # Extract all links from the page
            elements = driver.find_elements(By.TAG_NAME, "a")
            links = {urljoin(website_url, elem.get_attribute("href")) for elem in elements if elem.get_attribute("href")}
            
            print(f"Extracted {len(links)} links from {website_url}")
            driver.quit()
            return True, list(links)
        except WebDriverException as e:
            print(f"Failed to open website: {website_url}, Error: {str(e)}")
            return False, []
    
    @staticmethod
    def extract_text_selenium(url):
        """
        Extracts text content from a given URL.
        """
        try:
            driver = SeleniumScraperServices.init_web_driver()
            if not driver:
                return ""
            
            print(f"Extracting text from: {url}")
            driver.get(url)
            time.sleep(5)
            
            # Extract text from the body tag
            text = driver.find_element(By.TAG_NAME, "body").text
            print(f"Extracted text length: {len(text)} characters")
            
            driver.quit()
            return text
        except WebDriverException as e:
            print(f"Error extracting text from {url}: {str(e)}")
            return ""
    
    @staticmethod
    def get_links_selenium_get_response_data(website_url):
        """
        Extracts links from the given website and fetches text from each link.
        """
        link_status, links = SeleniumScraperServices.get_links_selenium(website_url)
        
        if not link_status:
            return False, f"Failed to open website: {website_url}", []
        
        extracted_data = []
        for link in links:
            try:
                text = SeleniumScraperServices.extract_text_selenium(link)
                if text:
                    extracted_data.append(text)
            except Exception as e:
                print(f"Error extracting text from {link}: {str(e)}")
        
        print(f"Extracted data from {len(extracted_data)} URLs")
        return True, "Data extraction complete", extracted_data
