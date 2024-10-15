import os
import pandas as pd

def find_most_recent_file(directory):
    # Find the most recently modified file in the specified directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def process_duplicates_in_column(file_path, column_index=3):
    # Read the CSV file, assuming no headers so we use header=None
    df = pd.read_csv(file_path, header=None)
    
    # Check if the specified column index is valid
    if column_index >= df.shape[1]:
        print(f"Error: The file only has {df.shape[1]} columns, but column {column_index + 1} was requested.")
        return
    
    # Select the column based on the provided index (columns are zero-indexed in pandas)
    column_data = df.iloc[:, column_index]
    
    # Create a dictionary to track occurrences of each entry
    occurrences = {}
    
    # Iterate over each row in the column and append count to duplicates
    for i, value in column_data.items():
        if value in occurrences:
            occurrences[value] += 1
            # Append " #<number>" to the duplicate value
            df.iloc[i, column_index] = f"{value} #{occurrences[value]}"
        else:
            occurrences[value] = 1

    # Overwrite the original file with the modified dataframe
    df.to_csv(file_path, index=False, header=False)
    print(f"Processed and overwritten the file: {file_path}")

if __name__ == "__main__":
    input_directory = r"C:\Users\Public\Documents\CBwhole"
    
    # Find the most recent file in the directory
    recent_file = find_most_recent_file(input_directory)
    
    # Process the file for duplicates in column 4 (zero-indexed as column 3)
    process_duplicates_in_column(recent_file)
