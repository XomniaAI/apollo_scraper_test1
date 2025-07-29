from datetime import datetime
import os
import random
import time
import pandas as pd
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

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv('APOLLO_EMAIL')
PASSWORD = os.getenv('APOLLO_PASSWORD')
URL = os.getenv('APOLLO_URL')

class ApolloScraper:
    def __init__(self, user_agents, url):
        '''Initialize the scraper with user agents, login credentials, and URL.'''
        self.user_agents = user_agents
        self.url = url
        self.driver = self.setup_webdriver()

    def setup_webdriver(self):
        '''Set up the Chrome WebDriver with random user-agent headers.'''
        service = Service()
        options = Options()
        options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        return self.driver

    def login(self):
        '''Perform login to the Apollo website using email and password.'''
        print("🔄 Navigating to Apollo login page...")
        
        # Go directly to login page first (like colleague's solution)
        self.driver.get("https://app.apollo.io/#/login")
        time.sleep(5)  # Wait for page to load
        
        print("📧 Entering credentials...")
        
        # Use colleague's simple approach - direct CSS selectors, no clear()
        try:
            # Enter email
            email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
            email_input.send_keys(EMAIL)
            print(f"✅ Email entered: {EMAIL}")
            
            # Enter password  
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            password_input.send_keys(PASSWORD)
            print("✅ Password entered")
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            print("✅ Login button clicked")
            
            print("⏳ Logging in, please wait for Apollo to load after login...")
            time.sleep(10)  # Wait for login to complete
            
            # Now navigate to the actual search page
            print("🔄 Navigating to search results page...")
            self.driver.get(URL)  # Use the search URL from .env
            time.sleep(7)  # Wait for results to load
            
            print("✅ Successfully logged in and navigated to search page!")
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print("🔍 Taking screenshot for debugging...")
            self.driver.save_screenshot("debug_login_error.png")
            print("📸 Screenshot saved as 'debug_login_error.png'")
            raise

    def get_text_or_default(self, element, default=''):
        '''Helper function to extract text from an element or return default if None.'''
        return element.text.strip() if element else default

    def scrape_data(self, num_pages_to_scrape, excel_file_path):
        '''Scrape data from the Apollo website and save it to an Excel file.'''
        page_num = 0

        print("Starting to scrape! :)")

        while page_num < num_pages_to_scrape:
            page_num += 1
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Initialize the data dictionary for this page
            page_data = {
                'Full Name': [],
                'Job Title': [],
                'Company': []
            }

            # Extracting names
            name_elements = soup.select('div[data-testid="contact-name-cell"] a')
            full_names = []
            for name_elem in name_elements:
                full_name = name_elem.get_text().strip()
                if full_name:
                    full_names.append(full_name)
                    

            # Extracting job titles
            titles = [self.get_text_or_default(title) for title in soup.find_all('span', class_='zp_Y6y8d')[::3]]

            # Extracting company names
            company_names = [self.get_text_or_default(name.find('a'), "Company not found") for name in soup.find_all('div', class_='zp_J1j17')]

            # Storing the scraped data in the dictionary
            page_data['Full Name'].extend(full_names)
            page_data['Job Title'].extend(titles)
            page_data['Company'].extend(company_names)
            
            # Save the data for this page
            df = pd.DataFrame(page_data)
            self.save_to_excel(df, excel_file_path)

            # Proceed to next page if available
            if page_num < num_pages_to_scrape:
                try:
                    print(f'Scraping page {page_num}/{num_pages_to_scrape}.')
                    next_page_button = self.driver.find_element(By.XPATH, '//*[@id="main-app"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div/div/div[3]/div/div[2]/button[2]')
                    next_page_button.click()
                    time.sleep(3)
                except NoSuchElementException:
                    print("No next page button found.")
                    break

    def save_to_excel(self, df, excel_file_path):
        '''Save the scraped data to an Excel file. If file exists, it appends new data.'''
        if os.path.isfile(excel_file_path):
            existing_df = pd.read_excel(excel_file_path)
            df_no_duplicates = pd.concat([existing_df, df]).drop_duplicates(keep='last')
            df_no_duplicates.to_excel(excel_file_path, index=False)
        else:
            df.to_excel(excel_file_path, index=False)
        print(f"Data saved to {excel_file_path}")

    def remove_duplicates(self, input_file, output_file):
        '''Remove duplicate entries in the Excel file and save the cleaned data.'''
        df = pd.read_excel(input_file)
        if df.duplicated().any():
            df_no_duplicates = df.drop_duplicates()
            df_no_duplicates.to_excel(output_file, index=False)
            print(f"Duplicate rows removed and saved to {output_file}")
        else:
            df.to_excel(output_file, index=False)
            print("No duplicate rows found. Data remains unchanged.")

    def quit(self):
        '''Close the WebDriver session.'''
        self.driver.quit()


if __name__ == "__main__":
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"]

    scraper = ApolloScraper(user_agents, URL)

    scraper.login()

    num_pages_to_scrape = int(os.getenv('PAGES_TO_SCRAPE', 5))  # Convert to int with fallback
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file_path = f"data_{timestamp}.csv"
    
    scraper.scrape_data(num_pages_to_scrape, excel_file_path)

    scraper.quit()

