import os
import pandas as pd
import glob

def find_most_recent_folder(directory):
    # Find the most recently modified folder in the specified directory
    all_folders = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    latest_folder = max(all_folders, key=os.path.getmtime)
    return latest_folder

def get_csv_files(directory):
    # Get all the CSV files in the specified directory
    return glob.glob(os.path.join(directory, "*.csv"))

def construct_output_filename(input_file):
    # Get the output file name by removing all characters after 'f' in the name
    base_name = os.path.basename(input_file)
    name_without_extension = os.path.splitext(base_name)[0]
    new_name = name_without_extension.split('f')[0] + "whole.csv"
    return new_name

def combine_csv_files(input_folder, output_folder):
    # Retrieve the CSV files from the most recent folder
    csv_files = get_csv_files(input_folder)
    
    # Sort the files in order of frag1 to frag5
    frag_order = ['frag1', 'frag2', 'frag3', 'frag4', 'frag5']
    sorted_files = []
    
    for frag in frag_order:
        for file in csv_files:
            if frag in file:
                sorted_files.append(file)
                break
    
    # Read the first CSV to get the first 7 columns and set the output file name
    first_file = sorted_files[0]
    first_df = pd.read_csv(first_file, header=None)
    
    # Extract the first 7 columns (common across all files)
    result_df = first_df.iloc[:, :7]
    
    # Add columns 8-19 from frag1 to frag4, and columns 8-17 from frag5
    for i, file in enumerate(sorted_files):
        df = pd.read_csv(file, header=None)
        if i < 4:  # frag1 to frag4
            result_df = pd.concat([result_df, df.iloc[:, 7:19]], axis=1)
        else:  # frag5
            result_df = pd.concat([result_df, df.iloc[:, 7:17]], axis=1)
    
    # Set the output filename
    output_file_name = construct_output_filename(first_file)
    output_file_path = os.path.join(output_folder, output_file_name)
    
    # Save the result without headers
    result_df.to_csv(output_file_path, index=False, header=False)
    print(f"Combined CSV file saved at: {output_file_path}")

if __name__ == "__main__":
    input_directory = r"C:\Users\Public\Documents\CBfrags"
    output_directory = r"C:\Users\Public\Documents\CBwhole"
    
    # Find the most recent folder and combine the CSVs
    recent_folder = find_most_recent_folder(input_directory)
    combine_csv_files(recent_folder, output_directory)