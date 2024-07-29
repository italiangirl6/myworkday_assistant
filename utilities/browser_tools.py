import os
import platform
import sys
import requests
from lxml import html
import tarfile
import zipfile

class BrowserDrivers:

    def __init__(self):
        self.os_type = self.get_os()
        self.driver_path = os.path.join("drivers", "geckodriver")
        if os.name == 'nt':
            self.driver_path += ".exe"
        os.makedirs("drivers", exist_ok=True)
    
    def get_os(self):
        return platform.system().lower()

    def get_firefox_version(self):
        if self.os_type == 'windows':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Mozilla\Mozilla Firefox')
            version, _ = winreg.QueryValueEx(key, "CurrentVersion")
        elif self.os_type == 'linux':
            version = os.popen('firefox -v').read().strip().split(' ')[-1]
        else:
            raise NotImplementedError(f"OS '{self.os_type}' is not supported.")
        return version

    def download_geckodriver(self):
        url = "https://github.com/mozilla/geckodriver/releases/latest"
        response = requests.get(url)
        redirected_url = response.url
        
        # Extract the version string from the redirected URL
        version = redirected_url.rstrip('/').split('/')[-1]
        # response = requests.get(redirected_url)
        # tree = html.fromstring(response.content)
        
        # Debug: Print the redirected URL
        print("Redirected URL:", redirected_url)
        print("Version Number:", version)

        # Debug: Print a portion of the HTML content
        # print("HTML content snippet:", response.content[:1000])  # Print the first 1000 characters


        if self.os_type == 'windows':
            download_url = f"https://github.com/mozilla/geckodriver/releases/download/{version}/geckodriver-{version}-win64.zip"
        elif self.os_type == 'linux':
            download_url = f"https://github.com/mozilla/geckodriver/releases/download/{version}/geckodriver-{version}-linux64.tar.gz"
        else:
            raise NotImplementedError(f"OS '{self.os_type}' is not supported.")

        # download_url = tree.xpath(xpath)[0].get('href')
        # full_url = f"https://github.com{download_url}"
        full_url = download_url
        
        file_name = full_url.split('/')[-1]
        print(f'Full Url > {full_url} -\nFile Name = {file_name}')
        save_path = os.path.join("drivers", file_name)
        
        response = requests.get(full_url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        self.extract_and_clean(save_path)

    def extract_and_clean(self, file_path):
        if file_path.endswith('.tar.gz'):
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(path="drivers")
            os.remove(file_path)
        elif file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall("drivers")
            os.remove(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    def get_yes_no_input(self, prompt):
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in ['y', 'n']:
                return user_input
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


    def check_and_download_geckodriver(self):
        if not os.path.isfile(self.driver_path):
            print("# - The Firefox driver was not found, this is necessary for the app to work.\n")
            continue_download = self.get_yes_no_input('Do you want to Download the Driver? (y/n) ')
            if continue_download == 'y':
                # TODO : Handle version better if it becomes a problem
                # firefox_version = self.get_firefox_version()
                # print(f"Your Computers Firefox Version: {firefox_version}")
                self.download_geckodriver()
                print("\nThe Firefox Driver has been downloaded and extracted. \n(If your Firefox Browser updates you will need to update under Settings)")
            else:
                print(f'Quiting Application.')
                sys.exit(0)
        # else:
        #     print("Geckodriver is already present.")


