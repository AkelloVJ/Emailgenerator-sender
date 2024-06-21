import pandas as pd

def clean_emails(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Filter out emails with less than 15 characters
    df = df[df['EmailAddress'].str.len() >= 17]

    # Write the filtered DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = "uncleanmails1.csv"
    output_file = "cleaned_mails.csv"
    clean_emails(input_file, output_file)
