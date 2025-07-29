import os
import random
import time
import pandas as pd
from datetime import datetime
from itertools import zip_longest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Import Cloudflare bypass libraries
try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv('APOLLO_EMAIL')
PASSWORD = os.getenv('APOLLO_PASSWORD')
URL = os.getenv('APOLLO_URL')

class ApolloScraper:
    def __init__(self, user_agents, url, bypass_method="stealth"):
        '''Initialize the scraper with user agents, login credentials, and URL.
        
        bypass_method options:
        - "stealth": Use selenium-stealth (recommended)
        - "undetected": Use undetected-chromedriver
        - "basic": Use basic selenium with anti-detection
        - "advanced": Combine multiple techniques
        '''
        self.user_agents = user_agents
        self.url = url
        self.bypass_method = bypass_method
        self.driver = self.setup_webdriver()

    def setup_webdriver(self):
        '''Set up the Chrome WebDriver with Cloudflare bypass techniques.'''
        print(f"🛡️ Setting up WebDriver with bypass method: {self.bypass_method}")
        
        if self.bypass_method == "stealth" and STEALTH_AVAILABLE:
            return self._setup_stealth_driver()
        elif self.bypass_method == "undetected" and UNDETECTED_AVAILABLE:
            return self._setup_undetected_driver()
        elif self.bypass_method == "advanced":
            return self._setup_advanced_driver()
        else:
            return self._setup_basic_driver()

    def _setup_stealth_driver(self):
        '''Setup driver with selenium-stealth (most effective for Cloudflare)'''
        print("🥷 Using Selenium Stealth method...")
        
        service = Service()
        options = Options()
        
        # Enhanced user agent rotation
        user_agent = random.choice(self.user_agents)
        options.add_argument(f"user-agent={user_agent}")
        
        # Anti-detection arguments from ScrapeOps guide
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")  # Faster loading
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Apply stealth settings
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="MacIntel",  # Match your actual platform
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris Pro OpenGL Engine",
            fix_hairline=True,
        )
        
        # Remove selenium automation properties
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.maximize_window()
        return driver

    def _setup_undetected_driver(self):
        '''Setup driver with undetected-chromedriver'''
        print("🔓 Using Undetected ChromeDriver method...")
        
        # Configure undetected chrome options
        options = uc.ChromeOptions()
        
        user_agent = random.choice(self.user_agents)
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        # Create undetected driver
        driver = uc.Chrome(options=options, version_main=None)
        driver.maximize_window()
        return driver

    def _setup_advanced_driver(self):
        '''Setup driver with advanced anti-detection techniques'''
        print("⚡ Using Advanced anti-detection method...")
        
        service = Service()
        options = Options()
        
        # Multiple user agents for rotation
        user_agent = random.choice(self.user_agents)
        options.add_argument(f"user-agent={user_agent}")
        
        # Comprehensive anti-detection arguments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--mute-audio")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        
        # Disable automation indicators
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Additional prefs to look more human
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,
                "media_stream": 2,
            },
            "profile.managed_default_content_settings": {
                "images": 2  # Block images for faster loading
            }
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute scripts to remove automation traces
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        
        driver.maximize_window()
        return driver

    def _setup_basic_driver(self):
        '''Setup basic driver with minimal anti-detection'''
        print("🔧 Using Basic anti-detection method...")
        
        service = Service()
        options = Options()
        
        user_agent = random.choice(self.user_agents)
        options.add_argument(f"user-agent={user_agent}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()
        return driver

    def human_like_delay(self, min_delay=1, max_delay=3):
        '''Add human-like random delays'''
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def simulate_human_behavior(self):
        '''Simulate human-like behavior to avoid detection'''
        # Random mouse movements (using JavaScript)
        self.driver.execute_script("""
            var event = new MouseEvent('mousemove', {
                'view': window,
                'bubbles': true,
                'cancelable': true,
                'clientX': arguments[0],
                'clientY': arguments[1]
            });
            document.dispatchEvent(event);
        """, random.randint(100, 500), random.randint(100, 500))
        
        # Random scroll
        self.driver.execute_script(f"window.scrollTo(0, {random.randint(100, 300)});")
        self.human_like_delay(0.5, 1.5)

    # STEPS 1 & 2: Login and navigate to search page
    def step1_and_2_login_and_navigate(self):
        '''STEPS 1-2: Login to Apollo and navigate to search page.'''
        print("🔄 STEP 1-2: Login and Navigation with Anti-Detection")
        print("=" * 50)
        
        try:
            # Go directly to login page first
            print("🌐 Navigating to Apollo login page...")
            self.driver.get("https://app.apollo.io/#/login")
            
            # Simulate human behavior after page load
            self.human_like_delay(3, 6)
            self.simulate_human_behavior()
            
            print("📧 Entering credentials with human-like behavior...")
            
            # Enter email with realistic delays
            email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
            self.simulate_human_behavior()
            
            # Type email character by character to mimic human typing
            for char in EMAIL:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            self.human_like_delay(1, 2)
            
            # Enter password
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            self.simulate_human_behavior()
            
            # Type password character by character
            for char in PASSWORD:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            self.human_like_delay(2, 4)
            self.simulate_human_behavior()
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            
            print("⏳ Waiting for login to complete with extended delay...")
            # Extended wait for Cloudflare challenges
            self.human_like_delay(10, 15)
            
            # Check if we need to handle Cloudflare challenge
            self._handle_cloudflare_challenge()
            
            # Navigate to search page
            print("🔄 Navigating to search results page...")
            self.driver.get(URL)
            self.human_like_delay(8, 12)
            self.simulate_human_behavior()
            
            print("✅ STEPS 1-2 COMPLETED: Successfully logged in and navigated to search page!")
            return True
            
        except Exception as e:
            print(f"❌ STEPS 1-2 FAILED: {e}")
            # Take screenshot for debugging
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"extracted_data/debug_login_error_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Error screenshot saved: {screenshot_path}")
            raise

    def _handle_cloudflare_challenge(self):
        '''Handle Cloudflare challenge if it appears'''
        try:
            # Check for common Cloudflare challenge indicators
            cloudflare_indicators = [
                "Checking your browser before accessing",
                "This process is automatic",
                "DDoS protection by Cloudflare",
                "Please wait while we verify that you're a real person",
                "cf-browser-verification",
                "Ray ID"
            ]
            
            page_source = self.driver.page_source.lower()
            
            if any(indicator.lower() in page_source for indicator in cloudflare_indicators):
                print("🛡️ Cloudflare challenge detected! Waiting for automatic resolution...")
                
                # Wait longer for Cloudflare to resolve automatically
                max_wait = 30
                wait_time = 0
                
                while wait_time < max_wait:
                    self.human_like_delay(2, 4)
                    wait_time += 3
                    
                    # Check if challenge is resolved
                    current_url = self.driver.current_url
                    if "apollo.io" in current_url and "challenge" not in current_url.lower():
                        print("✅ Cloudflare challenge resolved automatically!")
                        return
                    
                    # Simulate human behavior while waiting
                    self.simulate_human_behavior()
                
                print("⚠️ Cloudflare challenge may still be active after 30 seconds")
            
        except Exception as e:
            print(f"⚠️ Error checking for Cloudflare challenge: {e}")

    # STEP 3: Get raw HTML from current page and create BeautifulSoup
    def create_soup(self, page_num):
        # Wait for page to fully load
        time.sleep(5)
        # Get raw HTML source
        raw_html = self.driver.page_source
        # Create BeautifulSoup object
        soup = BeautifulSoup(raw_html, 'html.parser')
        print(f"🍲 BeautifulSoup object created")
        
        # Debug: Save screenshot and HTML source
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"extracted_data/debug_live_page_{timestamp}_{page_num}.png"
        #html_path = f"extracted_data/debug_live_source_{page_num}.html"
        
        self.driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
        
        # with open(html_path, "w", encoding="utf-8") as f:
        #     f.write(raw_html)
        # print(f"💾 Raw HTML saved: {html_path}")
        
        print(f"✅ STEP 3 COMPLETED: BeautifulSoup object ready for filtering")
        return soup

    # STEP 4: Extract person rows (much simpler filtering)
    def step4_extract_person_rows(self, soup, page_num):
        '''STEP 4: Extract person rows from BeautifulSoup object.
        
        Input: soup (BeautifulSoup) - complete parsed HTML object
        Output: person_rows (list) - list of BeautifulSoup elements, each representing one person
        '''
        print(f"\n🔄 STEP 4: Extracting Person Rows")
        print("=" * 50)
        
        # Find all person rows using the exact pattern from the real HTML
        person_rows = soup.find_all('div', {'class': 'zp_Uiy0R', 'role': 'row'})
        print(f"🔍 Found {len(person_rows)} person rows")
        
        if len(person_rows) == 0:
            print("⚠️  WARNING: No person rows found!")
            # Save debug file for inspection
            with open(f"debug_no_person_rows_{page_num}.html", "w", encoding="utf-8") as f:
                f.write(str(soup))
    
        print(f"✅ STEP 4 COMPLETED: Found {len(person_rows)} person rows to process")
        return person_rows

    # STEP 5: Extract contact data from person rows (completely rewritten)
    def step5_extract_contact_data(self, person_rows):
        '''STEP 5: Extract names, job titles, and companies from person rows.
        
        Input: person_rows (list) - list of BeautifulSoup elements for each person
        Output: contact_data (dict) - extracted contact information
        '''
        print(f"\n🔄 STEP 5: Extracting Contact Data from {len(person_rows)} person rows")
        print("=" * 50)
        
        names = []
        job_titles = []
        companies = []
        
        for idx, person_row in enumerate(person_rows, 1):            
            # Get all cells, but exclude the checkbox cell (has zp_xk8LG class)
            all_cells = person_row.find_all('div', {'role': 'cell', 'class': 'zp_egyXf'})
            data_cells = [cell for cell in all_cells if 'zp_xk8LG' not in cell.get('class', [])]
            
            if len(data_cells) < 3:
                print(f"  ⚠️  Person {idx}: Only {len(data_cells)} data cells found, skipping")
                continue
            
            # Extract data from the first 3 cells
            name_cell = data_cells[0]
            job_title_cell = data_cells[1] 
            company_cell = data_cells[2]
            
            # Extract name from first cell
            name = self._extract_name_from_cell(name_cell)
            names.append(name)
            
            # Extract job title from second cell
            job_title = self._extract_job_title_from_cell(job_title_cell)
            job_titles.append(job_title)
            
            # Extract company from third cell
            company = self._extract_company_from_cell(company_cell)
            companies.append(company)
        
        # Create structured contact data
        contact_data = self._create_structured_data(names, job_titles, companies)
        
        print(f"✅ STEP 5 COMPLETED: Extracted data for {len(names)} contacts")
        return contact_data

    def _extract_name_from_cell(self, name_cell):
        """Extract name from the name cell using the exact pattern."""
        try:
            # Pattern: div[data-testid="contact-name-cell"] a
            name_element = name_cell.select_one('div[data-testid="contact-name-cell"] a')
            if name_element:
                name = name_element.get_text().strip()
                return name if name else "Unknown Name"
            else:
                print("    ⚠️  Name element not found")
                return "Unknown Name"
        except Exception as e:
            print(f"    ⚠️  Error extracting name: {e}")
            return "Unknown Name"
    
    def _extract_job_title_from_cell(self, job_title_cell):
        """Extract job title from the job title cell, prioritizing NEW values when changes exist."""
        try:
            # PRIORITY 1: Check for NEW job title (when person changed jobs)
            # Pattern: span.zp_pMqXp span.zp_xvo3G (the updated value)
            new_title_element = job_title_cell.select_one('span.zp_pMqXp span.zp_xvo3G')
            if new_title_element:
                new_job_title = new_title_element.get_text().strip()
                if new_job_title:
                    print(f"    🔄 Found NEW job title: {new_job_title}")
                    return new_job_title
            
            # FALLBACK: Original extraction logic (when no changes)
            # Pattern: span.zp_FEm_X (original job title)
            original_title_element = job_title_cell.select_one('span.zp_FEm_X')
            if original_title_element:
                job_title = original_title_element.get_text().strip()
                if job_title:
                    return job_title
                
            print("    ⚠️  No job title element found")
            return "Unknown Title"
            
        except Exception as e:
            print(f"    ⚠️  Error extracting job title: {e}")
            return "Unknown Title"

    def _extract_company_from_cell(self, company_cell):
        """Extract company from the company cell, prioritizing NEW values when changes exist."""
        try:
            # PRIORITY 1: Check for NEW company (when person changed companies)
            # Pattern: span.zp_pMqXp span.zp_xvo3G (the updated value)
            new_company_element = company_cell.select_one('span.zp_pMqXp span.zp_xvo3G')
            if new_company_element:
                new_company = new_company_element.get_text().strip()
                if new_company:
                    print(f"    🔄 Found NEW company: {new_company}")
                    return new_company
            
            # FALLBACK: Original extraction logic (when no changes)
            # Pattern: span.zp_xvo3G (original company)
            original_company_element = company_cell.select_one('span.zp_xvo3G')
            if original_company_element:
                company = original_company_element.get_text().strip()
                if company:
                    return company
                    
            print("    ⚠️  Company element not found")
            return "Unknown Company"
            
        except Exception as e:
            print(f"    ⚠️  Error extracting company: {e}")
            return "Unknown Company"
    
    def _create_structured_data(self, names, job_titles, companies):
   
        # Determine max length
        max_length = max(len(names), len(job_titles), len(companies))
        
        if max_length == 0:
            print("⚠️  No contact data found!")
            return None
        
        # Pad lists to same length with empty strings
        names.extend([''] * (max_length - len(names)))
        job_titles.extend([''] * (max_length - len(job_titles)))
        companies.extend([''] * (max_length - len(companies)))
        
        # Create structured data
        contact_data = {
            'Full Name': names,
            'Job Title': job_titles,
            'Company': companies
        }
        
        return contact_data

    # STEP 6: Save page data to file
    def step6_save_data_to_file(self, contact_data, page_num, output_file):

        if contact_data is None:
            print("⚠️  No data to save, skipping...")
            return False

        # Create DataFrame
        df = pd.DataFrame(contact_data)
        
        try:
            if page_num == 1:
                # First page - create new file
                df.to_csv(output_file, index=False)
                print(f"📁 Created new CSV file: {output_file}")
            else:
                # Subsequent pages - append to existing file
                existing_df = pd.read_csv(output_file)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.to_csv(output_file, index=False)
                print(f"📁 Appended {len(df)} rows to: {output_file}")
            
            print(f"✅ STEP 6 COMPLETED: Data saved successfully")
            return True
            
        except Exception as e:
            print(f"❌ STEP 6 FAILED: {e}")
            # Save to backup file
            backup_file = f"{output_file}_page_{page_num}_backup.csv"
            df.to_csv(backup_file, index=False)
            print(f"💾 Saved to backup file: {backup_file}")
            return False

    # STEP 7: Navigate to next page
    def step7_navigate_to_next_page(self, current_page):
        try:
            print(f'Navigating from page {current_page} to page {current_page + 1}...')
            
            time.sleep(3)  # Wait for page to fully load
            success = False
            
            # Strategy 1: WORKING SELECTOR - aria-label="Next" (discovered from logs)
            try:
                next_page_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
                next_page_button.click()
                print("✅ Strategy 1 (aria-label='Next') worked!")
                time.sleep(2)
                success = True
            except Exception as e:
                print(f"❌ Strategy 1 (aria-label='Next') failed: {e}")
            
            if not success:
                # Strategy 2: More specific selector with class
                try:
                    next_page_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"].zp_NbJqo.zp_hgBYR')
                    next_page_button.click()
                    print("✅ Strategy 2 (specific Next button with classes) worked!")
                    time.sleep(3)
                    success = True
                except Exception as e:
                    print(f"❌ Strategy 2 (specific Next button with classes) failed: {e}")
            
            if success:
                print(f"✅ STEP 7 COMPLETED: Successfully navigated to page {current_page + 1}")
                return True
            else:
                print("❌ All strategies failed")
                return False
            
        except Exception as e:
            print(f"❌ STEP 7 FAILED: {e}")
            return False

    # MAIN ORCHESTRATOR: Run all steps in sequence
    def scrape_all_pages(self, num_pages_to_scrape, output_file):

        for page_num in range(1, num_pages_to_scrape + 1):

            try:
                # STEP 3: Get raw HTML and create BeautifulSoup object
                soup = self.create_soup(page_num)
                
                # STEP 4: Extract person rows from the soup
                person_rows = self.step4_extract_person_rows(soup, page_num)
                
                # STEP 5: Extract contact data from person rows
                contact_data = self.step5_extract_contact_data(person_rows)
                
                # STEP 6: Save data to file
                save_success = self.step6_save_data_to_file(contact_data, page_num, output_file)
                
                if not save_success:
                    print(f"⚠️  Page {page_num}: Save failed, but continuing...")
                
                # STEP 7: Navigate to next page (if not last page)
                if page_num < num_pages_to_scrape:
                    nav_success = self.step7_navigate_to_next_page(page_num)
                    if not nav_success:
                        print(f"⚠️  Cannot navigate further. Stopping at page {page_num}")
                        break
                
                print(f"✅ PAGE {page_num} COMPLETED SUCCESSFULLY")
                
            except Exception as e:
                print(f"❌ PAGE {page_num} FAILED: {e}")
                print("🔍 Taking error screenshot...")
                self.driver.save_screenshot(f"debug_error_page_{page_num}.png")
                # Continue to next page instead of stopping completely
                continue
        
        print(f"\n🎉 SCRAPING PROCESS COMPLETED!")

    def quit(self):
        '''Close the WebDriver session.'''
        print("\n🔒 CLOSING BROWSER SESSION")
        self.driver.quit()
        print("✅ Browser closed successfully")


if __name__ == "__main__":
    # Enhanced user agents that are less likely to be detected
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

    # Choose bypass method - try different ones if one doesn't work
    bypass_methods = ["stealth", "undetected", "advanced", "basic"]
    
    for method in bypass_methods:
        try:
            print(f"\n🚀 ATTEMPTING BYPASS METHOD: {method.upper()}")
            print("=" * 60)
            
            scraper = ApolloScraper(user_agents, URL, bypass_method=method)
            
            # STEPS 1 & 2: Login and navigate to search page
            if scraper.step1_and_2_login_and_navigate():
                print(f"✅ {method.upper()} method successful for login!")
                
                # Configuration
                num_pages_to_scrape = int(os.getenv('PAGES_TO_SCRAPE', 1))  # Start with 1 page for testing
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                excel_file_path = f"extracted_data/data_{timestamp}.csv"
                
                # STEPS 3-8: Scrape all pages (repeated for each page)
                scraper.scrape_all_pages(num_pages_to_scrape, excel_file_path)
                
                # Close browser
                scraper.quit()
                
                print(f"🎉 SUCCESS WITH {method.upper()} METHOD!")
                break  # Exit loop if successful
            
        except Exception as e:
            print(f"❌ {method.upper()} method failed: {e}")
            try:
                scraper.quit()
            except:
                pass
            
            if method == bypass_methods[-1]:  # Last method
                print("❌ All bypass methods failed!")
            else:
                print(f"🔄 Trying next method...")
                time.sleep(5)  # Wait before trying next method