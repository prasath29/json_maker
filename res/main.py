import pandas as pd
import os
import csv
import ast
import shutil  # For creating the .zip file

# Load the Excel file that is presented in the same directory
df = pd.read_excel("Brain File without Duplicate Intents.xlsx", sheet_name="Pivot Table 1", engine="openpyxl")

# Step 1: Fill down the first column to remove expand buttons (merged cells that is to remove the expand buttons)
df.iloc[:, 0] = df.iloc[:, 0].ffill()

# Step 2: Group by the first column and collect all related values from the second column into a list
grouped_df = df.groupby(df.columns[0])[df.columns[1]].agg(list).reset_index()

# Step 3: Save the result to a new Excel file to be used in the next step
grouped_df.to_excel("Grouped_Intents_with_Questions.xlsx", index=False)

print("==============Step 1 Completed ==============")

# Input the previous step Excel file as a input
input_file = "Grouped_Intents_with_Questions.xlsx"

# Specify the Output directory to save the CSV files
output_dir = "output_csv"
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Reads the Excel file
df = pd.read_excel(input_file)

# Filter rows where column B is not empty and does not contain '[nan]'
filtered_df = df[df.iloc[:, 1].notna() & (df.iloc[:, 1] != '[nan]')]  # Assuming column B is the second column (index 1)

# Iterate through the filtered rows and create CSV files
for index, row in filtered_df.iterrows():
    file_name = row.iloc[0]  # Assuming column A contains the file name to be used for the CSV file name
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
        for value in values:  # Iterate through the values list
            writer.writerow([value])  # Write each value in column B as a new row

# Compress the output directory into a .zip file
zip_file = "output_csv.zip"
shutil.make_archive("output_csv", 'zip', output_dir)

print(f"CSV files have been created in the '{output_dir}' directory.")
print(f"The directory '{output_dir}' has been compressed into '{zip_file}'.")