# selenium_operations.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

class SeleniumOperations:
    driver = None

    def __init__(self):
        if SeleniumOperations.driver is None:
            chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
            chrome_binary_path = os.getenv("CHROME_BINARY_PATH")
            chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
            chrome_profile_directory = os.getenv("CHROME_PROFILE_DIRECTORY")

            service = Service(executable_path=chrome_driver_path)
            options = webdriver.ChromeOptions()
            options.binary_location = chrome_binary_path

            # Uncomment the following line if you want to run Chrome headless
            # options.add_argument("--headless")

            options.add_argument("--no-sandbox")
            options.add_argument('--disable-gpu')

            options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
            options.add_argument(f'--profile-directory={chrome_profile_directory}') 

            SeleniumOperations.driver = webdriver.Chrome(service=service, options=options)

    def get_current_window_handle(self):
        return SeleniumOperations.driver.current_window_handle

    def go_to_url(self, url):
        SeleniumOperations.driver.get(url)

    def open_new_window_and_go_to_url(self, url):
        original_window = SeleniumOperations.driver.current_window_handle
        SeleniumOperations.driver.execute_script("window.open('about:blank', 'new window', 'width=800,height=600');")
        new_window = [window for window in SeleniumOperations.driver.window_handles if window != original_window][0]
        SeleniumOperations.driver.switch_to.window(new_window)
        SeleniumOperations.driver.get(url)