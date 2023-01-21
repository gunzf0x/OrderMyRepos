#!/usr/bin/python3

import argparse
import sys
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
import subprocess

# ANSI escape codes dictionary
colors = {
        "BLACK": '\033[30m',
        "RED": '\033[31m',
        "GREEN": '\033[32m',
        "BROWN": '\033[33m',
        "BLUE": '\033[34m',
        "PURPLE": '\033[35m',
        "CYAN": '\033[36m',
        "WHITE": '\033[37m',
        "GRAY": '\033[1;30m',
        "L_RED": '\033[1;31m',
        "L_GREEN": '\033[1;32m',
        "YELLOW": '\033[1;33m',
        "L_BLUE": '\033[1;34m',
        "PINK": '\033[1;35m',
        "L_CYAN": '\033[1;36m',
        "NC": '\033[m'
        }


# Define a simple character to print steps
sb: str = f'{colors["L_CYAN"]}[*]{colors["NC"]}'
whitespaces: str = " "*(len('[*]')+1)

def parse_args():
    """
    Simple function to get flags given by the user
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add an argument called "--flag" with action "store_true"
    parser.add_argument("-w", "--webpage", type=str, help="Webpage to extract the content. For example, a Github repository url (without .git at the end of it)")
    parser.add_argument("-c", "--clone", action="store_true",
                        help="Use this flag if you want to, additionally, clone the repository on your machine.")
    parser.add_argument("-f", "--filename", type=str, default="repositories.txt",
                        help="File to write the content extracted. If not specified, it will be saved in './repositories.txt' as default")
    parser.add_argument("-x", "--html-class", type=str, default="f4 my-3", help="HTML class containing the description for the repository (default in Github: 'f4-my3')")

    # Parse the command-line arguments
    args = parser.parse_args(sys.argv[1:])

    check_arguments_length(parser)

    return args


def check_arguments_length(parser_variable) -> None:
    """
    Check if the arguments provided by the user are valid
    """
    if len(sys.argv) > 1:
        return
    if len(sys.argv) <= 1:
        print(f"Invalid argument length: {len(sys.argv)}")
        parser_variable.error(f"Arguments provided must be more than {len(sys.argv)}")
        sys.exit(1)


def check_HTTP_status_code(webpage_var: str, html_class_var: str) -> str:
    """
    Check HTTP status code for a web request. If it exists return its content, else executes an error
    """
    # Send an HTTP request to the URL requested by the user
    print(f"{sb} Sending HTTP request to {webpage_var}...")
    r = requests.get(webpage_var)

    # Check HHTP status code. If the page does not responds, exit and print the HTTP status code
    if r.status_code != 200:
        print("Error: HTTP status code {r.status_code}")
        sys.exit(1)


    # Get the HTML content of the webpage
    soup = BeautifulSoup(r.text, "lxml")

    # Find all the div elements with the class "item"
    items = soup.find_all(class_=html_class_var)

    # Check how many items have been return and, in function of that, display a certain message
    if len(items) > 1:
        print(f"{sb}Warning! More than 1 items found. Found {len(items)} items.")
        print("{sb}This script will only return the first item found. However, ", end='')
        print("all the items found are:")

    if len(items) == 1:
        print(f"{sb} Description found!\n")

    if len(items) == 0:
        print(f"{sb} No description found")
        return 'NO DESCRIPTION'

    # Create a simple array that will store the description string
    fixed_description = []

    # Print the text of each items
    for i, item in enumerate(items):
        # Each description may have spaces before and after words, so filter them with split function and rebuild the description
        word_list = item.text.split()
        description: str = ''
        for j, word in enumerate(word_list):
            if j != len(word_list)-1:
                description += f"{word} "
            else:
                description += word
        # Print the 'rebuilt' description
        if len(items) == 1:
            print(f'{colors["RED"]}[{colors["YELLOW"]}+{colors["RED"]}] {colors["L_GREEN"]}"{description}"{colors["NC"]}')
            fixed_description.append(description)
            break
        else:
            print(f'{whitespaces}{colors["RED"]}{i+1}) "{description}"{colors["NC"]}')
        fixed_description.append(description)
    print("")
    return fixed_description[0]


def check_file_to_write(args_var, description: str) -> None:
    """
    Checks if the file to write the output exists. If it exists, add a line. If not, creates it.
    """
    file_to_append = Path.cwd().joinpath(args_var.filename)
    
    # The following string will be added to the file given by the user
    description_to_add = f"{args_var.webpage}.git -- {description}\n"

    # Get path to the file
    file_path = Path(file_to_append)

    # If the file provided by the user does not exists, create a new one
    if not file_path.exists():
        print(f"{sb} {colors['RED']}Warning{colors['NC']}: '{file_to_append}' does not exist. ", end='')
        create_file = input(f"Would you like to create '{file_path.name}' file? {colors['YELLOW']}[Y/N]{colors['NC']}: ")
        if re.match(r"^y(es)?$", create_file, re.IGNORECASE): # re.IGNORECASE is case-insensitive, i.e., 'yes = YeS'
            with open(file_to_append, 'x') as f: # 'x' will raise an error if the file already exists
                f.write(description_to_add)
            print(f"{sb} Description added to the recently created file '{file_to_append}'")
            return
        elif re.match(r"^n(o)?$", create_file, re.IGNORECASE):
            print(f"{sb} No file will be created. Exiting...")
            sys.exit(1)
        else:
            print(f"{sb} Error: No valid argument provided. Exiting...")
            sys.exit(1)

    if file_path.exists():
        # Check if the repository has not been already/previously added
        with open(file_to_append, 'r') as f:
            lines = f.readlines()

            # Check if the first column is already present
            is_repo_already_added = any(line.startswith(args_var.webpage) for line in lines)

        # If the repository has not been previously added, add it 
        if not is_repo_already_added:
            with open(file_to_append, 'a') as f:
                f.write(description_to_add)
                print(f"{sb} Description added to file!")
        # If the repository has been previously added finish the program with an error
        if is_repo_already_added:
            print(f"{sb} {args_var.webpage} has already been added. Exiting...")
            sys.exit(1)
    return


def clone_repo(args_var) -> None:
    """
    Clone the repository if the user passed the flag '--clone' or '-c'
    """
    if args_var.clone:
        print(f"{sb} Cloning {args_var.webpage}.git...")
        clone_command = subprocess.run(["git", "clone", f"{args_var.webpage}.git"])
        if clone_command.returncode == 0:
            print(f"{sb} Repository cloned succesfully!")
        else:
            print(f"{sb} {colors['RED']}Warning:{colors['NC']}Failed when trying to clone the repository...")
    return


def main():
    """
    MAIN
    """
    args = parse_args()
    description_obtained = check_HTTP_status_code(args.webpage, args.html_class) 
    check_file_to_write(args_var=args, description=description_obtained, )
    clone_repo(args_var=args)
    print(f"{sb} Done!")

if __name__ == "__main__":
    main()
