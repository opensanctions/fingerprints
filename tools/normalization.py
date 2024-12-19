import csv

file_path = "tools/statements.csv"
output_file_path = "tools/filtered_results.csv"

try:
    # Open and read the input CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Open the output CSV file for writing
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            fieldnames = ['value', 'original_value', 'lang']  # Define the output CSV column headers
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)

            # Write header to the output CSV file
            writer.writeheader()

            # Iterate over rows and filter for 'name' in the 'prop' column
            for i, row in enumerate(reader):
                if i >= 5000:  # Stop after processing x rows
                    break
                if row["prop"] == "name" and row["schema"] in ["Company", "Organization"]:
                    # Write the filtered row to the output CSV file
                    writer.writerow({'value': row['value'], 
                            'original_value': row['original_value'],
                                     'lang': row['lang']})

    print(f"Filtered results have been saved to {output_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
