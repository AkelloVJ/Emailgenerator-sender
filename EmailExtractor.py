import re
import csv

def extract_emails(input_file, output_csv):
    # Read existing emails from the uncleanmails.csv file to check for duplicates
    existing_emails = set()
    try:
        with open(output_csv, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_emails.update(row[0] for row in csv_reader)
    except FileNotFoundError:
        pass  # File doesn't exist yet

    # Open the output2.txt file and extract emails
    with open(input_file, 'r', encoding='utf-8') as text_file:
        text_content = text_file.read()

    # Use a regular expression to find emails containing '@gmail.com'
    emails = re.findall(r'\b\w+@gmail\.com\b', text_content)

    # Filter out duplicates
    unique_emails = set(emails) - existing_emails

    # Append unique emails to the uncleanmails.csv file
    with open(output_csv, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for email in unique_emails:
            csv_writer.writerow([email])

if __name__ == "__main__":
    input_file = "output2.txt"
    output_csv = "uncleanmails1.csv"

    extract_emails(input_file, output_csv)
