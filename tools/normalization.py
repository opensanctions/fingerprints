import csv

file_path = "tools/statements.csv"
output_file_path = "tools/company_names.csv"

try:
    # Open and read the input CSV file
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Open the output CSV file for writing
        with open(
            output_file_path, mode="w", newline="", encoding="utf-8"
        ) as output_file:
            fieldnames = [
                "entity_id",
                "prop",
                "prop_type",
                "value",
                "lang",
                "original_value",
                "schema",
            ]
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)

            # Write header to the output CSV file
            writer.writeheader()

            # Iterate over rows and filter for 'name' in the 'prop' column
            # for i, row in enumerate(reader):
            # if i >= 5000:  # Stop after processing x rows
            #     break
            for row in reader:
                if row["prop_type"] == "name" and row["schema"] in [
                    "Company",
                    "Organization",
                ]:
                    writer.writerow(
                        {
                            "entity_id": row["entity_id"],
                            "prop": row["prop"],
                            "prop_type": row["prop_type"],
                            "value": row["value"],
                            "lang": row["lang"],
                            "original_value": row["original_value"],
                            "schema": row["schema"],
                        }
                    )

    print(f"Filtered results have been saved to {output_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
