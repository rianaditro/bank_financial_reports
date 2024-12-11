import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException as SERE
from selenium.common.exceptions import WebDriverException as WDE


class Crawler:
    def __init__(self, mode:str):
        self.options = Options()
        self.options.add_argument("--headless")
        # self.options.add_argument("--start-maximized")

        prefs = {"profile.default_content_settings.popups": 0,    
        "download.default_directory":fr"/home/rianaditro/projects/data_scraping/ojk/{mode}",
        "download.prompt_for_download": False, 
        "download.directory_upgrade": True}

        self.options.add_experimental_option("prefs", prefs)
        self.download_folder = mode

        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def restart_driver(self):
        if self.driver:
            try:
                print("Driver restart")
                self.driver.quit()
            except WDE as e:
                print(f"Error quitting WebDriver: {e}")
            finally:
                self.driver = webdriver.Chrome(options=self.options)
                self.wait = WebDriverWait(self.driver, 10)
    
    def monitoring_download(self, filename:str):
        existing_files = set(os.listdir(self.download_folder))
        wait_time = 1
        status_code = 0

        while True:
            print("waiting download")
            time.sleep(wait_time)
            wait_time += 1

            current_files = set(os.listdir(self.download_folder))
            new_file = current_files - existing_files

            if new_file: # DEBUG: This should be only one
                os.rename(f"{self.download_folder}/{list(new_file)[0]}", f"{self.download_folder}/{filename}")
                print(f"{filename} downloaded")
                status_code = 1
                return status_code

            if wait_time > 10:
                print(f"Download time exceed: {self.driver.current_url}")
                break
        return status_code
    
    def find_until_clickable(self, ID:str):
        return self.wait.until(
            EC.element_to_be_clickable((By.ID, ID))
        )

    def get_excel(self, data:dict):
        """Opening the url and clicking the excel download button"""
        url = data['file_url']
        filename = data['filename']

        self.driver.get(url)
        print(f"Opening {url}")

        if "object" in self.driver.title:
            return "object_reference_error"
        elif "tidak tersedia" in self.driver.page_source:
            print(f"Laporan Tidak Tersedia: {url}")
            return "not_exist"
        else:
            self.find_until_clickable("CFSReportViewer_ctl05_ctl04_ctl00_ButtonLink").click()
            self.driver.find_element(By.LINK_TEXT, "Excel").click()
            status_code = self.monitoring_download(filename)

            if status_code:
                return "downloaded"
            else:
                return "download_incomplete"
