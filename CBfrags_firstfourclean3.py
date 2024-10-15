import os
import pandas as pd
import glob  # Importing the glob library

def fill_empty_columns(df):
    """
    Fills empty cells in columns 6 and 7 with the value from column 3 in the same row.
    """
    # Iterate over each row
    for index, row in df.iterrows():
        # If column 6 (index 5) is empty, fill it with the value from column 3 (index 2)
        if pd.isna(row[5]):
            df.at[index, 5] = row[2]
        # If column 7 (index 6) is empty, fill it with the value from column 3 (index 2)
        if pd.isna(row[6]):
            df.at[index, 6] = row[2]

    return df

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
    all CSV files that contain "frag1", "frag2", "frag3", or "frag4" in their names.
    """
    # Get the most recently modified folder
    recent_folder = get_most_recent_folder(base_directory)
    
    if recent_folder is None:
        print(f"No subdirectories found in {base_directory}")
        return

    # Define search patterns for the "frag" segments
    search_patterns = ["*frag1*.csv", "*frag2*.csv", "*frag3*.csv", "*frag4*.csv"]
    
    # Loop through all search patterns and get matching files
    for pattern in search_patterns:
        matching_files = glob.glob(os.path.join(recent_folder, pattern))
        
        # Process each matching file
        for file_path in matching_files:
            print(f"Processing file: {file_path}")

            # Load the CSV file without headers into a DataFrame
            df = pd.read_csv(file_path, header=None)

            # Fill empty columns 6 and 7 with data from column 3
            df = fill_empty_columns(df)

            # Save the modified DataFrame back to the file without a header
            df.to_csv(file_path, header=False, index=False)

# Usage:
base_directory = r"C:\Users\Public\Documents\CBfrags"
modify_files_in_most_recent_folder(base_directory)