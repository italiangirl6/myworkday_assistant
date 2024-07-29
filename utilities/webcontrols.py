import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from cryptography.fernet import Fernet

from content.workday_objects import WorkdayDOMObjects as _wdo
from utilities.web_tools import WebTools



class WebControls:
    def __init__(self, db_path='ledger.db'):
        self.db_path = db_path
        self.driver = self.setup_driver()
        self._wt = WebTools(self.driver)

    def setup_driver(self):
        options = FirefoxOptions()
        options.headless = True
        options.add_argument("--headless") 
        driver_path = os.path.join(os.getcwd(), 'drivers', 'geckodriver.exe')
        
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"Firefox Driver not found at {driver_path}")
        if not os.access(driver_path, os.X_OK):
            raise PermissionError(f"Firefox driver at {driver_path} is not executable")
        
        service = webdriver.FirefoxService(executable_path=driver_path)
        return webdriver.Firefox(service=service, options=options)


    def get_credentials(self, target_url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM entries WHERE url=?', (target_url,))
        entry = cursor.fetchone()
        conn.close()
        if entry:
            encrypted_password = entry
            key = self.load_key()
            fernet = Fernet(key)
            try:
                encrypted_password = encrypted_password.encode('utf-8') if isinstance(encrypted_password, str) else encrypted_password
                # salted_password = fernet.decrypt(encrypted_password[0]).decode('utf-8')
                # password = salted_password[24:]  # remove salt

                salted_password = fernet.decrypt(encrypted_password[0])
                password = salted_password[16:].decode('utf-8')  # remove salt
                return password
            except Exception as e:
                print(f"Error decrypting password: {e}")
                return None
        return None


    def load_key(self):
        key_file = 'secret.key'
        with open(key_file, 'rb') as f:
            return f.read()


    def login(self, entry_id):
        url = entry_id[1]
        job_title = entry_id[3]
        job_salary = entry_id[4]
        username = entry_id[5]
        password = self.get_credentials(url)
        if not password:
            print("Something went wrong, password decryption failed?")
            return
        self.driver.get(url)

        try:
            # Fill out the Login Form then click Submit
            self._wt.wait_for_element_to_appear(By.XPATH, _wdo.login_username, 10)
            self._wt.enter_text(By.XPATH, _wdo.login_username, username)
            self._wt.enter_text(By.XPATH, _wdo.login_password, password)
            self._wt.emulate_click(By.XPATH, _wdo.login_submit)
            time.sleep(1)
            attempts_login = 0
            while True:
                submit_exists = self._wt.check_if_element_exists(By.XPATH, _wdo.login_submit)
                if attempts_login == 5: self.driver.quit
                if submit_exists:
                    self._wt.emulate_click(By.XPATH, _wdo.login_submit)
                    time.sleep(1)
                    ++attempts_login
                else:
                    break

            

            # TODO : Handle multiple applying for now just get first entry
            # TODO : Some titles are not urls which breaks the script
            # Check if we have any active, if no this means rejection may have occured
            time.sleep(1) # Prevent false positive
            no_apps_exists = self._wt.get_text(By.XPATH, _wdo.you_have_no_label, timeout=10)
            if no_apps_exists:
                return [f'- {job_title} ', f'[REJECTED]', f'( - )']
            else:
                # Collect the data we need
                self._wt.wait_for_element_to_appear(By.XPATH, _wdo.one_entry_status, timeout=20)
                # job_count = self._wt.get_element_count(By.XPATH, _wdo.table_rows)
                # self._wt.wait_for_element_to_appear(By.XPATH, _wdo.one_entry_title, timeout=20)
                # sub_title = self._wt.get_text(By.XPATH, _wdo.one_entry_title)
                sub_status = self._wt.get_text(By.XPATH, _wdo.one_entry_status)
                sub_date = self._wt.get_text(By.XPATH, _wdo.one_entry_submit_date)
                return [f'- {job_title} ({job_salary})', f'[{sub_status}]', f'({sub_date})']
        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()
        finally:
            self.driver.quit()


if __name__ == "__main__":
    wc = WebControls()
    # wc.login(1)  # Example entry ID

