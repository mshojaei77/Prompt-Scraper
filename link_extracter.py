#link_extracter.py

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_links_to_csv(links, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows([[link] for link in links])

# Set up the Chrome driver service
service = Service(executable_path="C:/chromedriver.exe")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service)

# Navigate to the URL
url = 'https://prompthero.com/midjourney-prompts'
driver.get(url)

# Use explicit wait for the presence of an element (you may adjust the timeout)
wait = WebDriverWait(driver, 30)

# Initialize an empty set to store unique links
unique_links = set()

try:
    # Continue extracting links until "You've reached the end!" is found
    while True:
        # Wait for the presence of the next link
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'prompt-card-a')))
        
        # Get the HTML content after the page is loaded
        html_input = driver.page_source
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_input, 'html.parser')
        
        # Find all links with the specified format
        links = soup.find_all('a', class_='prompt-card-a')
        
        # Extract the href attribute and append to the set
        for link in links:
            href = link.get('href')
            full_link = f'https://prompthero.com{href}'
            unique_links.add(full_link)
            print(f'Extracted link: {full_link}')
        
        # Check if "You've reached the end!" is present
        if soup.find(text="You've reached the end!"):
            print("Reached the end of prompts.")
            break
        
        # Scroll down to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolling down...")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

    # Convert the set to a list for writing to CSV
    all_links = list(unique_links)

    # Write the links to a CSV file
    csv_file_path = 'prompt_links.csv'
    save_links_to_csv(all_links, csv_file_path)

    print(f'Links have been saved to {csv_file_path}.')
