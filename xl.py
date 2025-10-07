import os
import pandas as pd
import csv
import ast  # To safely evaluate string representations of lists

# Input Excel file
input_file = "Grouped_Intents_with_Questions.xlsx"

# Output directory
output_dir = "output_csv"
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Read the Excel file
df = pd.read_excel(input_file)

# Filter rows where column B is not empty and does not contain '[nan]'
filtered_df = df[df.iloc[:, 1].notna() & (df.iloc[:, 1] != '[nan]')]  # Assuming column B is the second column (index 1)

# Iterate through the filtered rows and create CSV files
for index, row in filtered_df.iterrows():
    file_name = row.iloc[0]  # Assuming column A contains the file name
    column_b_value = row.iloc[1]  # Extract the value from column B
    
    # Safely evaluate the string representation of the list in column B
    try:
        values = ast.literal_eval(column_b_value) if isinstance(column_b_value, str) else [column_b_value]
    except (ValueError, SyntaxError):
        values = [column_b_value]  # If not a valid list, treat as a single value
    
    # Create the output CSV file path
    output_file = os.path.join(output_dir, f"{file_name}.csv")
    
    # Write to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow([file_name])  # Write the file name in column A
        for value in values:
            writer.writerow([value])  # Write each value in column B as a new row

print(f"CSV files have been created in the '{output_dir}' directory.")