from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import pandas as pd
import os
import re
from itertools import repeat

def zip_longest(*iterables, fillvalue=None):
    iterators = list(map(iter, iterables))
    num_active = len(iterators)
    if not num_active:
        return

    while True:
        values = []
        for i, iterator in enumerate(iterators):
            try:
                value = next(iterator)
            except StopIteration:
                num_active -= 1
                if not num_active:
                    return
                iterators[i] = repeat(fillvalue)
                value = fillvalue
            values.append(value)
        yield tuple(values)

def setup_webdriver():
    service = Service()
    options = Options()
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    # options.add_argument("--headless")  # Add this line for headless mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


def login(driver, email, password):
    driver.get(URL)

    email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'email')))
    email_input.click()
    email_input.send_keys(email)

    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
    password_input.click()
    password_input.send_keys(password)

    log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="provider-mounter"]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div/form/div[4]/button')))
    log_in_button.click()

    time.sleep(5)


def scrape_data(driver, num_pages_to_scrape):
    page_num = 0

    all_data = {
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

    print("Starting to scrape! :)")

    while page_num < num_pages_to_scrape:
        page_num += 1

        web_page = driver.page_source
        soup = BeautifulSoup(web_page, 'html.parser')

        # --------------------- FIRST AND LAST NAME --------------------- #
        # names = soup.find_all('div', class_='zp_xVJ20')

        # first_name = []
        # last_name = []

        # for name in names:
        #     anchor = name.find('a')
        #     if anchor:
        #         full_name = anchor.text.strip()
        #         split_name = full_name.split(' ', 1) 
        #         first_name.append(split_name[0])  
        #         if len(split_name) > 1:
        #             last_name.append(split_name[1])  
        #         else:
        #             last_name.append('')  

        names = (name.text.split(maxsplit=1) for name in soup.find_all('div', class_='zp_xVJ20') if name.find('a'))

        first_name, last_name = zip_longest(*names, fillvalue='')

        # --------------------- WEBSITE --------------------- #
        websites = soup.find_all('a', class_='zp-link zp_OotKe')
        website_list = []
        for website in websites:
            if website is not None:  # Check if website is not None
                href = website.get('href')
            if href and not href.startswith('#') and ("facebook" not in href and "linkedin" not in href and "twitter" not in href):
                website_list.append(href)

        # --------------------- COMPANY LINKEDIN --------------------- #
        websites = soup.find_all('a', class_='zp-link zp_OotKe')
        company_linkedin_list = []
        for website in websites:
            if website is not None:  # Check if website is not None
                href = website.get('href')
            if href and not href.startswith('#') and "linkedin" in href and "company" in href: 
                company_linkedin_list.append(href)

        # --------------------- PERSONAL LINKEDIN --------------------- #
        websites = soup.find_all('a', class_='zp-link zp_OotKe')
        personal_linkedin_list = []
        for website in websites:
            if website is not None:  # Check if website is not None
                href = website.get('href')
            if href and not href.startswith('#') and "linkedin" in href and "company" not in href: 
                personal_linkedin_list.append(href)

        # --------------------- INDUSTRY --------------------- #
        industries = soup.find_all('span', class_='zp_PHqgZ zp_TNdhR')
        industries = soup.find_all('span', class_='zp_PHqgZ zp_TNdhR')[:25]  # Limit to 25 elements
        industries_list = [industry.text.strip() for industry in industries if industry is not None]

        # --------------------- LOCATION --------------------- #
        locations = soup.find_all('span', class_='zp_Y6y8d')
        locations_list = [location.text.strip() for location in locations if location is not None and "Australia" in location.text.strip()]


        # --------------------- TITLE --------------------- #
        titles = soup.find_all('span', class_='zp_Y6y8d')
        titles_list = [title.text.strip() for title in titles[::3] if title is not None]

        # --------------------- COMPANY NAME --------------------- #
        company_names = soup.find_all('div', class_='zp_J1j17')
        company_names_clean = [name.find('a').text.strip() if name.find('a') is not None else "Company not found" for
                               name in company_names]

        # --------------------- PHONE NUMBERS --------------------- #
        phone_numbers = soup.find_all('span', class_='zp_lm1kV')
        phone_numbers_clean = [phone.find('a') for phone in phone_numbers]
        numbers = [phone.text.strip() for phone in phone_numbers_clean if phone is not None]


        # --------------------- EMAILS --------------------- #
        emails = soup.find_all('div', class_='zp_jcL6a')
        emails_list = [email.find('a', class_='zp-link zp_OotKe zp_Iu6Pf').text.strip() if email.find('a',
                                                                                                      class_='zp-link zp_OotKe zp_Iu6Pf') is not None else ''
                       for email in emails]

        all_data['Business Name'].extend(company_names_clean)
        all_data['Website'].extend(website_list)
        all_data['Niche'].extend(industries_list)
        all_data['Country'].extend(locations_list)
        all_data['First Name'].extend(first_name)
        all_data['Last Name'].extend(last_name)
        all_data['Job Title'].extend(titles_list)
        all_data['Phone number'].extend(numbers)
        all_data['Personal email'].extend(emails_list)
        all_data['Personal LinkedIn'].extend(personal_linkedin_list)
        all_data['Company LinkedIn'].extend(company_linkedin_list)

        # PRINT OUT WHAT IS THE LENGHT OF EACH COLUMN TO MAKE SURE THEY ARE THE SAME
        # for column, data_list in all_data.items():
        #     print(f"{column}: {len(data_list)}")

        # If not the last page, click the next page button
        if page_num < num_pages_to_scrape:
            try:
                next_page = driver.find_element(By.XPATH, '//*[@id="main-app"]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div/div/div[3]/div/div[2]/button[2]')
                next_page.click()
                time.sleep(3)
                print(f'Everything is still going as planned. Currently printing {page_num}/{num_pages_to_scrape}.')
            except NoSuchElementException:
                print("No button to click.")

    df = pd.DataFrame(all_data)
    return df


def save_to_excel(df, excel_file_path):
    if os.path.isfile(excel_file_path):
        existing_df = pd.read_excel(excel_file_path)

        # Check for duplicates in the existing DataFrame and the new data
        df_no_duplicates = pd.concat([existing_df, df]).drop_duplicates(keep='last')

        df_no_duplicates.to_excel(excel_file_path, index=False)
        print("Data saved to", excel_file_path)
    else:
        df.to_excel(excel_file_path, index=False)
        print("Data saved to", excel_file_path)


def remove_duplicates(input_file, output_file):
    df = pd.read_excel(input_file)
    if df.duplicated().any():
        df_no_duplicates = df.drop_duplicates()
        df_no_duplicates.to_excel(output_file, index=False)
        print("Duplicate rows removed and saved to", output_file)
    else:
        print("No duplicate rows found. Data remains unchanged.")


if __name__ == "__main__":
    URL = "YOUR APOLLO SAVED LIST LINK"

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"]

    driver = setup_webdriver()

    email = 'YOUR APOLLO EMAIL'
    password = 'YOUR APOLLO PASSWORD'
    login(driver, email, password)

    num_pages_to_scrape = 3
    scraped_data = scrape_data(driver, num_pages_to_scrape)

    excel_file_path = 'complete_data.xlsx'
    save_to_excel(scraped_data, excel_file_path)

    driver.quit()

    output_file_path = "output_file.xlsx"
    remove_duplicates(excel_file_path, output_file_path)
