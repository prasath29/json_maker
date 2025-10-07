import os
import pandas as pd
import csv

# Input Excel file
input_file = "groups.xlsx"

# Output directory
output_dir = "output_csv"
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Read the Excel file
df = pd.read_excel(input_file)

# Group by column A and aggregate all related values in column B
grouped = df.groupby(df.columns[0])[df.columns[1]].apply(list).reset_index()

# Iterate through the grouped data and create CSV files
for _, row in grouped.iterrows():
    file_name = row.iloc[0]  # Column A value (used as file name)
    values = [value for value in row.iloc[1] if pd.notna(value)]  # Filter out empty/NaN values
    
    # Skip creating a file if there are no valid values in the group
    if not values:
        continue
    
    # Create the output CSV file path
    output_file = os.path.join(output_dir, f"{file_name}.csv")
    
    # Write to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([file_name])  # Write the file name in column A
        for value in values:
            writer.writerow([value])  # Write each value in column B as a new row

print(f"CSV files have been created in the '{output_dir}' directory.")