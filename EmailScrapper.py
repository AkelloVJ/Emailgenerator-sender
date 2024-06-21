import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to sanitize the query for a file name
def sanitize_query(query):
    # Replace invalid characters with underscores
    sanitized_query = ''.join(c if c.isalnum() or c.isspace() else '_' for c in query)
    return sanitized_query.strip()

# Function to scrape visible text content from multiple pages
def scrape_visible_text(query, output_file):
    driver = webdriver.Chrome()
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
        print("No text content found.")
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

    with open(input_csv, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            query = row[0]
            scrape_visible_text(query, text_file)
