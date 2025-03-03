# start_screen.py
from colorama import Fore, Style, init
import search  # Importing the search module

# Initialize colorama for colored text output
init(autoreset=True)

# Looping the main menu
while True:
    # Printing a title for the program
    print(Fore.GREEN + "𝕷𝖔𝖘𝖙 𝖆𝖓𝖉 𝕱𝖔𝖚𝖓𝖉")

    # Adding ASCII art
    print(Fore.GREEN + r"""
       __...--~~~~~-._   _.-~~~~~--...__
        //               `V'               \\ 
       //                 |                 \\ 
      //__...--~~~~~~-._  |  _.-~~~~~~--...__\\ 
     //__.....----~~~~._\ | /_.~~~~----.....__\\
    ====================\\|//====================
                        `---`   
    """)

    # Displaying menu options
    print(Fore.CYAN + "1. Search")
    print(Fore.CYAN + "2. Help")
    print(Fore.RED + "99. Exit")

    # Getting user input
    choice = input(Fore.GREEN + "Please choose an option: ")

    # Handling the user's choice
    if choice == '1':
        target = input(Fore.GREEN + "Enter the email/target information to search for: ")
        file_or_folder = input(Fore.GREEN + "Enter the file or folder to search in: ")
        output_file = input(Fore.GREEN + "Enter the output file name: ")
        num_threads = input(Fore.GREEN + "Enter the number of threads (Default: 4): ")

        if target == '99' or file_or_folder == '99' or output_file == '99':
            continue

        num_threads = int(num_threads) if num_threads.isdigit() else 4  # Default to 4 threads
        search.search_files(target, file_or_folder, output_file, num_threads)

    elif choice == '2':
        print(Fore.CYAN + r"""How to Use:

Relative Path Example:
    file_or_folder input: example.txt
    - This will search for example.txt in the same directory as your script.

Absolute Path Example:
    file_or_folder input: C:\Users\YourName\Documents\example.txt (Windows)
    /home/username/Documents/example.txt (Linux/Mac)
    - This will search for the file in the specified directory.

Multithreading:
    - You can specify the number of threads to speed up the search.
    - Default is 4 threads. More threads = faster search but higher CPU usage.
    """)
        help_input = input(Fore.RED + "Press 99 to return to the main menu: ")
        if help_input == '99':
            continue

    elif choice == '99':
        print(Fore.RED + "Exiting!")
        break

    else:
        print(Fore.RED + "Invalid choice. Please select 1, 2, or 99 to exit.")
