
from datetime import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class WebTools():
    def __init__(self, driver):
        self.driver = driver


    def check_if_element_exists(self, how, what):
        try:
            self.driver.find_element(how, what)
            return True
        except NoSuchElementException:
            return False


    def click_element(self, how, what, timeout):
        self.wait_for_element_present(how, what, wait=2, timeout=timeout)
        self.driver.find_element(how, what).click()


    def click_element_with_js(self, element): 
        self.driver.execute_script("arguments[0].click();", element)


    def emulate_click(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            action = ActionChains(self.driver)  # Initialize ActionChains with self.driver
            action.double_click(element).perform()
        except TimeoutException as e:
            print(f"TimeoutException: {e}")
        except NoSuchElementException as e:
            print(f"NoSuchElementException: {e}")


    def enter_text(self, how, what, text):
        self.driver.find_element(how, what).clear()
        self.driver.find_element(how, what).send_keys(text)


    def get_element_count(self, by, value, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return len(elements)
        except TimeoutException:
            print(f"TimeoutException: Elements not found within {timeout} seconds.")
            return 0
        except NoSuchElementException:
            print("NoSuchElementException: Elements not found.")
            return 0


    def get_text(self, by, value, timeout=10) -> str:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element.text
        except TimeoutException:
            print(f"TimeoutException: Element not found within {timeout} seconds.")
            return ""
        except NoSuchElementException:
            print("NoSuchElementException: Element not found.")
            return ""


    def maximize_browser(self):
        self.driver.maximize_window()


    def navigate_to(self, url):
        try:
            self.driver.get(url)
        except TimeoutException as e:
            return f'Timed out on url: {e}'


    def press_enter(self):
        action = ActionChains(self)
        action.key_down(Keys.ENTER)
        action.key_up(Keys.ENTER)


    def press_tab(self):
        action = ActionChains(self)
        action.key_down(Keys.TAB)
        action.key_up(Keys.TAB)


    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)


    def wait_for_element_not_present(self, how, what, wait=1, timeout=60):
        for i in range(timeout):
            try:
                if not self.is_element_present(how, what): break
            except:
                pass
            time.sleep(wait)
        else:
            self.fail("time out")


    def wait_for_element_present(self, how, what, wait=1, timeout=60):
        for i in range(timeout):
            try:
                if self.is_element_present(how, what): break
            except:
                pass
            time.sleep(wait)
        else:
            self.fail(f'timed out ({timeout}) waiting for element present: {what}')


    def wait_for_element_to_appear(self, how, what, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout). \
                until(EC.presence_of_element_located((how, what)))
        except NoSuchElementException as e:
            return e
        return element
    

    def wait_for_element_to_disappear(self, by, value, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((by, value))
            )
            print(f"Obstructing element disappeared: {value}")
        except TimeoutException:
            print(f"Timeout while waiting for obstructing element to disappear: {value}")


    def wait_for_element_to_be_clickable(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            print(f"Element found and is clickable: {value}")
            return element
        except TimeoutException:
            print(f"Timeout while waiting for element to be clickable: {value}")
            return None
        except NoSuchElementException:
            print(f"Element not found: {value}")
            return None


    def wait_for_page_load(self, timeout=30):
        # Waits for the page to load by waiting for the given element to become stale 
        # (no longer attached to the DOM).
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        try:
            WebDriverWait(self.driver, timeout).until(staleness_of(old_page))
            print("Page loaded successfully.")
        except TimeoutException:
            print("Timeout while waiting for the page to load.")


    def wait_for_text_appear(self, how, what, target_text, timeout=60, wait=1):
        for i in range(timeout):
            try:
                if target_text == self.driver.find_element(how, what).text: break
            except:
                pass
            time.sleep(wait)
        else:
            self.fail("time out")