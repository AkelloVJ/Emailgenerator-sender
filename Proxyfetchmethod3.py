import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import extension
import requests

# Function to sanitize the query for a file name
def sanitize_query(query):
    # Replace invalid characters with underscores
    sanitized_query = ''.join(c if c.isalnum() or c.isspace() else '_' for c in query)
    return sanitized_query.strip()

# Function to scrape visible text content from multiple pages
def scrape_visible_text(driver, query, output_file):
    driver.get("https://www.google.com")

    # Locate the search input field and submit the query
    search_input = driver.find_element(By.NAME, 'q')
    search_input.clear()
    search_input.send_keys(query)
    search_input.submit()

    start_time = time.time()
    while time.time() - start_time < 20:  # Run for approximately 2 minutes
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust this time according to your need

    # Wait for text content elements to be present
    try:
        text_content_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tF2Cxc"))
        )
    except:
        print("No text content found for:", query)
        return

    # Extract the text content
    text_content = ' '.join(element.text for element in text_content_elements)

    # Append the text content to the output file
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(text_content + '\n')  # Append text content to the file

    print(f"Scraped data for '{query}'")

    # Move the queried item to searched.csv
    with open('searched.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([query])

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
    proxy_extension = extension.proxies(username, password, endpoint, port)

    # Open the browser once outside the loop
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(proxy_extension)
    driver = webdriver.Chrome(options=chrome_options)

    # Open the input CSV file in read mode
    with open(input_csv, 'r') as csvfile:
        # Read the CSV file
        csv_reader = csv.reader(csvfile)
        
        # Create a temporary list to store rows
        rows = list(csv_reader)

        # Iterate through each row in the CSV file
        for row in rows:
            # Extract the query from the row
            query = row[0]

            # Scrape visible text content for the query
            scrape_visible_text(driver, query, text_file)

        # Clear the input CSV file after scraping
        csvfile.seek(0)
        csvfile.truncate()

    # Close the browser after all queries are done
    driver.quit()
