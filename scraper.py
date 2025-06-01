import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_page_content(url: str) -> str:
    # ... your existing get_page_content function unchanged ...
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    driver = webdriver.Chrome(options=options)

    try:
        print(f"Scraping content from: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        try:
            wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        except TimeoutException:
            print("Warning: Page did not reach 'complete' readyState within 20 seconds.")

        elements = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6, p, ul, ol, pre, code, tr, th")
            )
        )

        content_parts = []
        for element in elements:
            try:
                tag = element.tag_name.lower()
                text = element.text.strip()
            except Exception as e:
                print(f"Warning: skipping element due to error: {e}")
                continue

            if text:
                if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    content_parts.append(f"\n{tag.upper()}: {text}\n")
                else:
                    content_parts.append(text)

        content = "\n\n".join(content_parts)

        if not content.strip():
            raise Exception("No meaningful content found on the page.")

        print(f"✅ Successfully extracted {len(content)} characters.")
        return content

    except Exception as e:
        print(f"❌ Error scraping page: {e}")
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <URL>")
        sys.exit(1)

    test_url = sys.argv[1]
    scraped_content = get_page_content(test_url)
    print("\n----- FULL PAGE CONTENT -----\n")
    print(scraped_content)
