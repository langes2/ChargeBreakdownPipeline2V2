import pandas as pd

def find_duplicates_in_column(file_path, column_index=3):
    # Read the CSV file, assuming no headers so we use header=None
    df = pd.read_csv(file_path, header=None)
    
    # Check if the specified column index is valid
    if column_index >= df.shape[1]:
        print(f"Error: The file only has {df.shape[1]} columns, but column {column_index + 1} was requested.")
        return
    
    # Select the column based on the provided index (columns are zero-indexed in pandas)
    column_data = df.iloc[:, column_index]
    
    # Find duplicated values in the selected column
    duplicates = column_data[column_data.duplicated(keep=False)]
    
    if duplicates.empty:
        print("No duplicates found in column 4.")
    else:
        print("Duplicates found in column 4:")
        print(duplicates)

if __name__ == "__main__":
    # Specify the path to the input CSV file
    file_path = r"C:\Users\Public\Documents\CBwhole\ChargeBreakdown10_10_24whole.csv"
    
    # Call the function to find duplicates in column 4 (index 3 in zero-based indexing)
    find_duplicates_in_column(file_path)
