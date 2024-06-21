import csv

def remove_common_queries(input_file, searched_file):
    # Read queries from input_queries.csv
    with open(input_file, 'r') as input_csv:
        input_reader = csv.reader(input_csv)
        input_queries = set(row[0] for row in input_reader)

    # Read queries from searched.csv
    with open(searched_file, 'r') as searched_csv:
        searched_reader = csv.reader(searched_csv)
        searched_queries = set(row[0] for row in searched_reader)

    # Remove common queries from input_queries.csv
    updated_queries = input_queries - searched_queries

    # Rewrite input_queries.csv without common queries
    with open(input_file, 'w', newline='') as output_csv:
        output_writer = csv.writer(output_csv)
        for query in updated_queries:
            output_writer.writerow([query])

# Main program
if __name__ == "__main__":
    input_file = "input_queries.csv"
    searched_file = "searched.csv"

    remove_common_queries(input_file, searched_file)
    print("Common queries removed from input_queries.csv")
