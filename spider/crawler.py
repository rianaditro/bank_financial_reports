import time
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler:
    def __init__(self):
        self.base_url = "https://ojk.go.id/id/kanal/perbankan/data-dan-statistik/laporan-keuangan-perbankan/Default.aspx"
        self.frame_url = "https://cfs.ojk.go.id/cfs/ReportViewerForm.aspx?"
        self.options = Options()
        # self.options.add_argument("--headless")
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)


    def _find_until_clickable(self, ID:str):
        return self.wait.until(
            EC.element_to_be_clickable((By.ID, ID))
        )

    def _get_valid_url(self, bank:str, year:int, month:int, report_code:str)->str:
        """Convert input to valid url"""
        # Split bank input
        bank_code, bank_name = bank.split("-", 1) # Max split is 1
        bank_name = bank_name.replace(" ", "+").replace(",", "%2C")

        # Change the report code for 2020+
        if year > 2020:
            report_code = report_code+"A"

        return f"{self.frame_url}BankCodeNumber={bank_code}&BankCode={bank_name}&Month={month}&Year={year}&FinancialReportPeriodTypeCode=B&FinancialReportTypeCode={report_code}"

    def get_excel(self, bank:str, year:int, month:int, report_code:str):
        url = self._get_valid_url(bank, year, month, report_code)        

        self.driver.get(url)

        self._find_until_clickable("CFSReportViewer_ctl05_ctl04_ctl00_ButtonLink").click()
        self.driver.find_element(By.LINK_TEXT, "Excel").click()

