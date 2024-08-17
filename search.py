import os
from PyPDF2 import PdfReader

def search_pdf(file_path, target, out_file):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and target in text:
                    out_file.write(f"Found in {file_path} (Page {page_num + 1}):\n{text}\n")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def search_files(target, file_or_folder, output_file):
    # Normalize the path to handle different OS
    file_or_folder = os.path.normpath(file_or_folder)
    output_file = os.path.normpath(output_file)

    # Check if the file or directory exists
    if not os.path.exists(file_or_folder):
        print(f"Error: The path '{file_or_folder}' does not exist.")
        return

    # Define the file extensions to search
    valid_extensions = ('.txt', '.py', '.pdf', '.html', '.xml', '.kt', '.java', '.smali')

    # Determine if we're searching a single file or a folder
    if os.path.isfile(file_or_folder):
        files_to_search = [file_or_folder]
    elif os.path.isdir(file_or_folder):
        # Get all relevant files in the folder
        files_to_search = [
            os.path.join(file_or_folder, f)
            for f in os.listdir(file_or_folder)
            if f.endswith(valid_extensions)
        ]
    else:
        print(f"Error: {file_or_folder} is neither a file nor a directory.")
        return

    total_files = len(files_to_search)

    # Open the output file in write mode
    with open(output_file, 'w') as out_file:
        for index, file_path in enumerate(files_to_search):
            try:
                if file_path.endswith('.pdf'):
                    search_pdf(file_path, target, out_file)
                else:
                    # Open each file and search for the target string
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line_num, line in enumerate(file, start=1):
                            if target in line:
                                out_file.write(f"{file_path} (Line {line_num}): {line}\n")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

            # Print progress
            percent_complete = (index + 1) / total_files * 100
            print(f"Progress: {percent_complete:.2f}%")

    print(f"Search complete. Results written to {output_file}")
