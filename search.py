# search.py

import os


def search_files(target, file_or_folder, output_file):
    # Normalize the path to handle different OS
    file_or_folder = os.path.normpath(file_or_folder)
    output_file = os.path.normpath(output_file)

    # Check if the file or directory exists
    if not os.path.exists(file_or_folder):
        print(f"Error: The path '{file_or_folder}' does not exist.")
        return

    # Determine if we're searching a single file or a folder
    if os.path.isfile(file_or_folder):
        files_to_search = [file_or_folder]
    elif os.path.isdir(file_or_folder):
        # Get all .txt files in the folder
        files_to_search = [
            os.path.join(file_or_folder, f)
            for f in os.listdir(file_or_folder) if f.endswith('.txt')
        ]
    else:
        print(f"Error: {file_or_folder} is neither a file nor a directory.")
        return

    # Open the output file in write mode
    with open(output_file, 'w') as out_file:
        for file_path in files_to_search:
            try:
                # Open each file and search for the target string
                with open(file_path, 'r') as file:
                    for line in file:
                        if target in line:
                            out_file.write(line)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    print(f"Search complete. Results written to {output_file}")