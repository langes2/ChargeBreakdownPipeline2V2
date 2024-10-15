import pandas as pd
import os
import glob

def modify_excel_file(input_file):
    # Load the Excel file
    df = pd.read_excel(input_file, header=None)
    
    # Drop the specified rows (row indices start from 0, so subtract 1)
    df = df.drop([0, 1, 3])

    # Drop the specified columns (column indices start from 0, so subtract 1)
    columns_to_drop = [4, 5, 7, 11, 14, 16, 19, 21]
    df = df.drop(df.columns[columns_to_drop], axis=1)

    # Find the row containing the phrase "Charge Breakdown (Summary)"
    phrase = "Charge Breakdown (Summary)"
    row_index = df[df.apply(lambda row: row.astype(str).str.contains(phrase, regex=False).any(), axis=1)].index
    
    if not row_index.empty:
        # Calculate the row from which to keep data
        cutoff_index = max(0, row_index[0] - 3)
        # Keep all rows up to three rows above the row with the phrase
        df = df[:cutoff_index]
    
    # Clean the DataFrame by applying the custom cleaning function
    df = clean_dataframe(df)
    
    # Save the modified and cleaned DataFrame to a CSV file without the header
    output_file = os.path.splitext(input_file)[0] + '.csv'
    df.to_csv(output_file, index=False, header=False)
    
    # Delete the original Excel file
    os.remove(input_file)

def clean_dataframe(df):
    """
    Cleans the DataFrame by:
    1. Removing rows where both the first and second columns are blank or NaN.
    2. Removing rows where the first column contains "Property Total", "Property Counts", 
       "Overall Total", or "Overall Counts".
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to be cleaned.
    
    Returns:
    pandas.DataFrame: The cleaned DataFrame.
    """
    # Drop rows where both the first and second columns are blank or NaN
    df_cleaned = df.dropna(subset=[df.columns[0], df.columns[1]], how='all')

    # Drop rows where the first column contains specific keywords
    keywords_to_remove = ['Property Total', 'Property Counts', 'Overall Total', 'Overall Counts']
    df_cleaned = df_cleaned[~df_cleaned[df.columns[0]].isin(keywords_to_remove)]

    return df_cleaned

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
        raise FileNotFoundError(f"No subdirectories found in {base_directory}")

    # Find the most recently modified subdirectory
    most_recent_folder = max(subdirectories, key=os.path.getmtime)
    
    return most_recent_folder

def main():
    # Define the base directory to search for the most recently modified folder
    base_directory = r"C:\Users\Public\Documents\CBfrags"
    
    # Get the most recently modified folder
    try:
        directory = get_most_recent_folder(base_directory)
    except FileNotFoundError as e:
        print(e)
        return

    # Define the search pattern for files that contain "frag5" in the filename
    search_patterns = ["*frag5*.xlsx"]
    
    # Loop through all search patterns
    for pattern in search_patterns:
        # Get the list of matching files
        list_of_files = glob.glob(os.path.join(directory, pattern))
        
        # Modify each file that matches the pattern
        for file in list_of_files:
            modify_excel_file(file)

if __name__ == "__main__":
    main()