import os
import random
import time
import pandas as pd
import re
from itertools import repeat, zip_longest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ApolloScraper:
    def __init__(self, user_agents, email, password, url):
        '''Initialize the scraper with user agents, login credentials, and URL.'''
        self.user_agents = user_agents
        self.email = email
        self.password = password
        self.url = url
        self.driver = self.setup_webdriver()

    def setup_webdriver(self):
        '''Set up the Chrome WebDriver with random user-agent headers.'''
        service = Service()
        options = Options()
        options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver

    def login(self):
        '''Perform login to the Apollo website using email and password.'''
        self.driver.get(self.url)
        email_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, 'email')))
        email_input.send_keys(self.email)

        password_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
        password_input.send_keys(self.password)

        log_in_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="provider-mounter"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div/form/div[4]/button')))
        log_in_button.click()

        time.sleep(5)

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
                'Business Name': [],
                'Website': [],
                'Niche': [],
                'Country': [],
                'First Name': [],
                'Last Name': [],
                'Job Title': [],
                'Phone number': [],
                'Personal email': [],
                'Personal LinkedIn': [],
                'Company LinkedIn': [],
            }

            # Extracting names
            names = [name.text.split(maxsplit=1) for name in soup.find_all('div', class_='zp_xVJ20') if name.find('a')]
            first_name, last_name = zip_longest(*names, fillvalue='')

            # Extracting websites
            websites = [a.get('href') for a in soup.find_all('a', class_='zp-link zp_OotKe')
                        if a.get('href') and not a.get('href').startswith('#') and not any(social in a.get('href') for social in ["facebook", "linkedin", "twitter", "apollo", "Facebook"])]
            company_names = [self.get_text_or_default(name.find('a'), "Company not found") for name in soup.find_all('div', class_='zp_J1j17')]
            websites.extend(["Website not specified"] * (len(company_names) - len(websites)))
            
            # Extracting company LinkedIn links
            company_linkedin_list = [a.get('href') for a in soup.find_all('a', class_='zp-link zp_OotKe')
                                     if a.get('href') and "linkedin" in a.get('href') and "company" in a.get('href')]
            company_linkedin_list.extend(["LinkedIn page not specified"] * (len(company_names) - len(company_linkedin_list)))
            
            # Extracting personal LinkedIn links
            personal_linkedin_list = [a.get('href') for a in soup.find_all('a', class_='zp-link zp_OotKe')
                                      if a.get('href') and "linkedin" in a.get('href') and "company" not in a.get('href')]

            # Extracting industries
            industries = soup.find_all('span', class_='zp_PHqgZ zp_TNdhR')[:25]
            industries_list = [industry.text.strip() for industry in industries if industry is not None]

            # Extracting locations
            locations = soup.find_all('span', class_='zp_Y6y8d')
            locations_list = [location.text.strip() for location in locations if location is not None and (location.text.strip().endswith(", Australia") or location.text.strip() == "Australia")]

            # Extracting job titles
            titles = [self.get_text_or_default(title) for title in soup.find_all('span', class_='zp_Y6y8d')[::3]]

            # Extracting company names
            company_names = [self.get_text_or_default(name.find('a'), "Company not found") for name in soup.find_all('div', class_='zp_J1j17')]

            # Extracting phone numbers
            phone_numbers = soup.find_all('span', class_='zp_lm1kV')
            phone_numbers_clean = [phone.find('a') for phone in phone_numbers]
            phone_numbers = [phone.text.strip() for phone in phone_numbers_clean if phone is not None]

            # Extracting emails
            emails = [self.get_text_or_default(email.find('a', class_='zp-link zp_OotKe zp_Iu6Pf')) for email in soup.find_all('div', class_='zp_jcL6a')]

            # Storing the scraped data in the dictionary
            page_data['Business Name'].extend(company_names)
            page_data['Website'].extend(websites)
            page_data['Niche'].extend(industries_list)
            page_data['Country'].extend(locations_list)
            page_data['First Name'].extend(first_name)
            page_data['Last Name'].extend(last_name)
            page_data['Job Title'].extend(titles)
            page_data['Phone number'].extend(phone_numbers)
            page_data['Personal email'].extend(emails)
            page_data['Personal LinkedIn'].extend(personal_linkedin_list)
            page_data['Company LinkedIn'].extend(company_linkedin_list)

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
    URL = "YOUR APOLLO SAVED LIST LINK"
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"]
    
    email = 'YOUR APOLLO EMAIL'
    password = 'YOUR APOLLO PASSWORD'

    scraper = ApolloScraper(user_agents, email, password, URL)

    scraper.login()

    num_pages_to_scrape = 2   # ENTER HOW MANY PAGES YOU WANT TO SCRAPE
    excel_file_path = 'data.xlsx'
    scraper.scrape_data(num_pages_to_scrape, excel_file_path)

    scraper.quit()

    output_file_path = "cleaned_data.xlsx"
    scraper.remove_duplicates(excel_file_path, output_file_path)
