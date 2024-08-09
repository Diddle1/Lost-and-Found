# start_screen.py
from colorama import Fore, Style, init
init(autoreset=True)
import search  # Importing the search module

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
        if target == '99' or file_or_folder == '99' or output_file == '99':
            continue
        search.search_files(target, file_or_folder, output_file)
    elif choice == '2':
        print(Fore.CYAN + r"""Relative Path Example:

file_or_folder input: example.txt
This will search for example.txt in the same directory where your Python script is running.

Absolute Path Example:

file_or_folder input: C:\Users\YourName\Documents\example.txt (Windows) or /home/username/Documents/example.txt (Linux/Mac)
This will search for example.txt in the specified directory.
    """)
        help_input = input(Fore.RED + "Press 99 to return to the main menu: ")
        if help_input == '99':
            continue
    elif choice == '99':
        print(Fore.RED + "Exiting!")
        break
    else:
        print("Invalid choice. Please select 1, 2, or 99 to exit.")