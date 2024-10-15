import os
import glob
import pandas as pd

def process_csv_in_place(file_path):
    # Load the CSV file without headers into a DataFrame
    df = pd.read_csv(file_path, header=None)

    # Step 1: Fill blanks in the first column by copying the data from the cell above
    df.iloc[:, 0] = df.iloc[:, 0].fillna(method='ffill')

    # Step 2: Take the 8-character suffix of the first row, first column
    first_row_suffix_1 = str(df.iloc[0, 0])[-8:]

    # Step 3: Create a new leftmost column and add the 8-character suffix for all rows with data
    df.insert(0, "NewLeftmost1", df.apply(lambda row: first_row_suffix_1 if pd.notna(row).any() else "", axis=1))

    # Step 4: Remove the 11-character suffix from the first row, first column
    df.iloc[0, 1] = str(df.iloc[0, 1])[:-11]  # Adjusting to column 1 because we added a new column at index 0

    # Step 5: Take the new 8-character suffix of the first row, first column (after removing the 11 characters)
    first_row_suffix_2 = str(df.iloc[0, 1])[-8:]

    # Step 6: Create another new leftmost column and add this new 8-character suffix for all rows with data
    df.insert(0, "NewLeftmost2", df.apply(lambda row: first_row_suffix_2 if pd.notna(row).any() else "", axis=1))

    # Step 7: Delete the first row
    df = df.drop(index=0).reset_index(drop=True)

    # Step 8: Remove rows that do not have data in the fourth column (index 3, as column indices start from 0)
    df = df.dropna(subset=[df.columns[3]])

    # Step 9: Save the modified DataFrame back to the file without a header
    df.to_csv(file_path, header=False, index=False)

def get_most_recent_folder(base_directory):
    """
    Returns the most recently modified folder within the base directory.
    
    Parameters:
    base_directory (str): The directory to search for subfolders.
    
    Returns:
    str: The path to the most recently modified folder.
    """
    # Get all subdirectories within the base directory
    subdirectories = [f.path for f in os.scandir(base_directory) if f.is_dir()]
    
    # Check if there are any subdirectories
    if not subdirectories:
        return None

    # Find the most recently modified subdirectory
    most_recent_folder = max(subdirectories, key=os.path.getmtime)
    
    return most_recent_folder

def modify_files_in_most_recent_folder(base_directory):
    """
    Finds the most recently modified folder in the base directory and processes 
    all CSV files that contain "frag5" in their names.
    """
    # Get the most recently modified folder
    recent_folder = get_most_recent_folder(base_directory)
    
    if recent_folder is None:
        print(f"No subdirectories found in {base_directory}")
        return

    # Define search patterns for the "frag" segments
    search_patterns = ["*frag5*.csv"]
    
    # Loop through all search patterns and get matching files
    for pattern in search_patterns:
        matching_files = glob.glob(os.path.join(recent_folder, pattern))
        
        # Process each matching file
        for file_path in matching_files:
            print(f"Processing file: {file_path}")
            process_csv_in_place(file_path)

# Usage:
base_directory = r"C:\Users\Public\Documents\CBfrags"
modify_files_in_most_recent_folder(base_directory)