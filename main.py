import argparse
import os
import sys
from utilities.db_tools import DBTools
from utilities.webcontrols import WebControls
from utilities.browser_tools import BrowserDrivers
import datetime

parser = argparse.ArgumentParser(description="Paramter to run script automatically.")
parser.add_argument('--auto_run', action='store_true', help='Runs Scripts')
args = parser.parse_args()

def print_header():
    print("""
 __  __     __        __         _       _
|  \/  |_   \ \      / /__  _ __| | ____| | __ _ _   _ 
| |\/| | | | \ \ /\ / / _ \| '__| |/ / _` |/ _` | | | |
| |  | | |_| |\ V  V / (_) | |  |   < (_| | (_| | |_| |
|_|  |_|\__, | \_/\_/ \___/|_|  |_|\_\__,_|\__,_|\__, |
        |___/                                    |___/ 
    _            _     _              _   
   / \   ___ ___(_)___| |_ __ _ _ __ | |_ 
  / _ \ / __/ __| / __| __/ _` | '_ \| __|
 / ___ \\__ \__ \ \__ \ || (_| | | | | |_ 
/_/   \_\___/___/_|___/\__\__,_|_| |_|\__|
        """)

def main():
    print_header()
    db = DBTools()
    bd = BrowserDrivers()
    auto_run = args.auto_run
    if auto_run:
        print(f'Auto Run Mode')
        bd.check_and_download_geckodriver()
        scan_statuses(db)
    else:
        while True:
            print("\nMenu:")
            print("1. Add new entry")
            print("2. Delete an entry")
            print("3. Run")
            print("4. Settings")
            print("5. Exit")

            choice = input("Select an option: ")

            if choice == '1':
                url = input("Enter URL: ")
                c_name = input("Enter Company Name: ")
                title = input("Enter Job Title: ")
                salary = input("(Leave Empty if not Provided)\nEnter Salary: ")
                username = input('Enter Username: ')
                password = input('\nEnter Password: ')
                db.add_entry(url, c_name, title, salary, username, password)
                print("Application Entry added successfully.")
            elif choice == '2':
                entries = db.get_entries()
                if not entries:
                    print('There were no entries found.')
                else:
                    for entry in entries:
                        print(f"{entry[0]}. {entry[2]} ({entry[3]})")
                    entry_id = int(input("Select the number of the entry to delete: "))
                    db.delete_entry(entry_id)
                    print("Entry deleted successfully.")
            elif choice == '3':
                bd.check_and_download_geckodriver()
                scan_statuses(db)
            elif choice == '4':
                print("\nSettings (This Section is under construction):")
                # print("1. Send data to API")
                # print("2. Print data to file")
                # settings_choice = input("Select an option: ")
                # entries = db.get_entries()
                # data = "\n".join([f"{datetime.datetime.now().strftime('%m/%d/%Y %H:%M')} - {entry[1]} ({entry[2]})" for entry in entries])
                # if settings_choice == '1':
                #     # Placeholder for sending data to API
                #     print("Sending data to API...")
                # elif settings_choice == '2':
                #     with open("status.log", "w") as file:
                #         file.write(data)
                #     print("Data written to status.log.")
            elif choice == '5':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")


def scan_statuses(database):
    entries = database.get_entries()
    if not entries:
        print("There are no entries to process.")
    else:
        status_data = []
        for entry in entries:
            print(f"Checking : {entry[2]}")
            # entry_id = int(input("Select the number of the entry to run: "))
            wc = WebControls()
            try:
                entry_info = wc.login(entry)
                entry_info.insert(0, entry[2])
                status_data.append(entry_info)
            except Exception as e:
                print(f"Error during login: {e}")
        clear_and_fill_log(status_data)
        print(f'\u2714 Complete: Please Check "status.log" for your Results.', flush=False)
    sys.exit(0)


def clear_and_fill_log(data_table):
    # Clear the log file
    log_file = 'status.log'
    with open(log_file, 'w') as file:
        pass

    # Iterate through rows and write to log file
    with open(log_file, 'a') as file:
        for e in data_table:
            submission = ' '.join(e)
            file.write(submission + "\n")


if __name__ == "__main__":
    main()

