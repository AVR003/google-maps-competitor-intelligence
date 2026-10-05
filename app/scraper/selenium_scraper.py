import os
import time
import logging
from typing import List, Dict, Any, Tuple
from app.ai.builtin_provider import classify_post

logger = logging.getLogger(__name__)

# Check if selenium and webdriver_manager are available
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except Exception as e:
    logger.warning(f"Selenium import issue: {e}")

class SeleniumGoogleMapsScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None

    def initialize_driver(self):
        if not SELENIUM_AVAILABLE:
            raise RuntimeError("Selenium is not available in current environment.")

        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(30)
            return True
        except Exception as e:
            logger.error(f"Failed to initialize ChromeDriver: {e}")
            self.driver = None
            return False

    def check_for_captcha(self) -> bool:
        if not self.driver:
            return False
        try:
            page_source = self.driver.page_source.lower()
            captcha_indicators = [
                "recaptcha",
                "g-recaptcha",
                "unusual traffic from your computer network",
                "our systems have detected unusual traffic",
                "verify you are a human",
                "cf-turnstile"
            ]
            for indicator in captcha_indicators:
                if indicator in page_source:
                    return True
        except Exception:
            pass
        return False

    def extract_updates_from_url(self, profile_url: str) -> Tuple[List[Dict[str, Any]], bool, str]:
        """
        Navigates to Google Maps profile, checks for captcha, and parses update posts.
        Returns: (posts_list, captcha_detected, error_message)
        """
        if not self.driver:
            if not self.initialize_driver():
                return [], False, "Could not initialize ChromeDriver (Falling back to adaptive parser)"

        try:
            self.driver.get(profile_url)
            time.sleep(3)

            # Check for CAPTCHA immediately
            if self.check_for_captcha():
                return [], True, "Google verification / CAPTCHA screen encountered"

            # Attempt to click Updates tab if present
            try:
                tabs = self.driver.find_elements(By.CSS_SELECTOR, "button[role='tab']")
                for tab in tabs:
                    if "update" in tab.text.lower() or "post" in tab.text.lower():
                        tab.click()
                        time.sleep(2)
                        break
            except Exception:
                pass

            # Extract post elements
            posts = []
            post_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.m6QEr, div[data-post-id], div.section-layout")
            for elem in post_elements[:10]:
                try:
                    text = elem.text.strip()
                    if len(text) > 20:
                        # Extract image if any
                        img_elems = elem.find_elements(By.TAG_NAME, "img")
                        img_urls = [img.get_attribute("src") for img in img_elems if img.get_attribute("src")]

                        classification = classify_post(text)
                        posts.append({
                            "text": text,
                            "date": "Recently scraped",
                            "cta": classification["cta"],
                            "topic": classification["topic"],
                            "keywords": classification["keywords"],
                            "images": img_urls[:2]
                        })
                except Exception:
                    continue

            return posts, False, ""

        except Exception as e:
            return [], False, str(e)

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
