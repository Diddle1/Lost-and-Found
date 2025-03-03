import os
import threading
from queue import Queue
from PyPDF2 import PdfReader
import mmap

# Lock for thread-safe progress updates
progress_lock = threading.Lock()
processed_files = 0  # Global counter for processed files


# Function to search within a PDF file
def search_pdf(file_path, target, results):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and target in text:
                    results.append(f"Found in {file_path} (Page {page_num + 1}):\n{text}\n")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


# Function to search within a text-based file
def search_text_file(file_path, target, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                if target in line:
                    results.append(f"{file_path} (Line {line_num}): {line}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


# Function to search within a large text-based file using mmap
def search_large_file(file_path, target, results):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            position = 0

            while position < len(mmapped_file):
                chunk = mmapped_file[position:position + 4096]  # Read 4KB chunks
                if target in chunk.decode('utf-8', errors='ignore'):
                    results.append(f"Found in {file_path} at position {position}")
                position += 4096

    except Exception as e:
        print(f"Error reading {file_path}: {e}")


# Worker function for threads
def worker(queue, target, results, total_files, large_files=False):
    global processed_files
    while not queue.empty():
        file_path = queue.get()
        
        if file_path.endswith('.pdf'):
            search_pdf(file_path, target, results)
        elif large_files and os.path.getsize(file_path) > 100 * 1024 * 1024:  # Check if file is larger than 100MB
            search_large_file(file_path, target, results)  # Use mmap for large files
        else:
            search_text_file(file_path, target, results)
        
        queue.task_done()

        # Update progress
        with progress_lock:
            processed_files += 1
            percentage = (processed_files / total_files) * 100
            print(f"Progress: {processed_files}/{total_files} ({percentage:.2f}%)", end='\r')


# Function to search files using multiple threads
def search_files(target, file_or_folder, output_file, num_threads=4, large_files=False):
    global processed_files
    valid_extensions = ('.txt', '.py', '.pdf', '.html', '.xml', '.kt', '.java', '.smali', '.json', '.properties')

    # Collect files to search
    files_to_search = []
    if os.path.isfile(file_or_folder):
        files_to_search.append(file_or_folder)
    elif os.path.isdir(file_or_folder):
        for root, _, files in os.walk(file_or_folder):
            for file in files:
                if file.endswith(valid_extensions):
                    files_to_search.append(os.path.join(root, file))

    total_files = len(files_to_search)
    if total_files == 0:
        print("No valid files found for searching.")
        return

    # Create queue and add files
    queue = Queue()
    for file in files_to_search:
        queue.put(file)

    results = []
    threads = []

    # Reset processed files counter
    processed_files = 0

    # Start threads
    for _ in range(min(num_threads, total_files)):
        thread = threading.Thread(target=worker, args=(queue, target, results, total_files, large_files))
        thread.start()
        threads.append(thread)

    # Wait for threads to complete
    for thread in threads:
        thread.join()

    # Write results to output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(results)

    print("\nSearch complete. Results written to", output_file)


