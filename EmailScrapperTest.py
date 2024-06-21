import os
import csv
import time
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from extension import proxies  # Importing the proxies function from extension.py

# Function to sanitize the query for a file name
def sanitize_query(query):
    # Replace invalid characters with underscores
    sanitized_query = ''.join(c if c.isalnum() or c.isspace() else '_' for c in query)
    return sanitized_query.strip()

# Function to scrape visible text content from multiple pages using proxies
def scrape_visible_text_with_proxies(query, output_file, proxy_extension):
    # Configure Chrome with the proxy extension
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(proxy_extension)
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://www.google.com")

    # Locate the search input field and submit the query
    search_input = driver.find_element(By.NAME, 'q')
    search_input.clear()
    search_input.send_keys(query)
    search_input.submit()

    start_time = time.time()  # Proper indentation here
    while time.time() - start_time < 40:  # Run for approximately 2 minutes
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(30)  # Adjust this time according to your need

    # Wait for text content elements to be present
    try:
        text_content_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tF2Cxc"))
        )
        rotate_proxy = True  # Set flag to rotate proxy if no exception occurs
    except:
        print("Error occurred. Rotating proxy...")
        driver.quit()
        return

    # Extract the text content
    text_content = ' '.join(element.text for element in text_content_elements)

    # Append the text content to the output file
    file_path = os.path.join(os.getcwd(), output_file)
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(text_content + '\n')  # Append text content to the file

    driver.quit()
    print(f"Scraped data for '{query}' and saved in '{file_path}'")

# Main program
if __name__ == "__main__":
    input_csv = "input_queries.csv"
    text_file = "output2.txt"  # Name of the output file
    
    # Define proxy credentials and endpoint
    username = 'user-spd3c4f42x-session-1-country-us'
    password = '24ea52Pqft=etrCyCD'
    endpoint = 'gate.smartproxy.com'
    port = 10001
    
    # Generate proxy extension
    proxy_extension = proxies(username, password, endpoint, port)

    with open(input_csv, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            query = row[0]
            while not scrape_visible_text_with_proxies(query, text_file, proxy_extension):
                # Retry scraping with a new proxy if error occurred
                proxy_extension = proxies(username, password, endpoint, port)
