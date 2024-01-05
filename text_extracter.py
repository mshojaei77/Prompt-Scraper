#text_extracter.py

import csv
import requests
from bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    prompt_tokens = soup.find('div', class_='the-prompt').find_all('a', class_='prompt-token')

    extracted_text = ", ".join(token.text.strip() for token in prompt_tokens)
    return extracted_text

def write_to_csv(data, file_path):
    with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write extracted texts
        csv_writer.writerows(data)

# Read links from prompt_links.csv
csv_file_path = 'prompt_links.csv'
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    links = [row[0] for row in csv_reader]

# Set a user agent to simulate a browser request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Initialize an empty set to store visited URLs
visited_urls = set()

# Initialize an empty list to store extracted texts
all_texts = []

# Create a session with retries
retries = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
with requests.Session() as session:
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # Loop through the links and extract text
    for index, link in enumerate(links, start=1):
        # Check if the URL has already been visited
        if link in visited_urls:
            print(f"Skipping duplicate URL: {link}")
            continue

        try:
            response = session.get(link, headers=headers)

            if response.status_code == 200:
                html_input = response.text

                # Call the function to extract text from HTML
                extracted_text = extract_text_from_html(html_input)
                all_texts.append([extracted_text])

                # Mark the URL as visited
                visited_urls.add(link)

                # Print progress
                print(f"Processed {index}/{len(links)} URLs - {link}")
            else:
                print(f"Failed to fetch content from {link}. Status code: {response.status_code}")

            # Add a delay of a few seconds
            time.sleep(3)  # Adjust the delay as needed to avoid rate-limiting

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {link}. Exception: {e}")

        # Write the extracted texts to a new CSV file after every 10 URLs
        if index % 10 == 0:
            write_to_csv(all_texts, 'partial_prompt_texts.csv')
            all_texts = []  # Clear the list after writing

# Write the remaining extracted texts to the final CSV file
write_to_csv(all_texts, 'prompt_texts.csv')

print('Texts have been saved to prompt_texts.csv.')
