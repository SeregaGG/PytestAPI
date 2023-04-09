import os.path
import requests
from selenium.webdriver.common.by import By
from .base_page import BasePage
import json
import ast
from selenium.webdriver.support.wait import WebDriverWait


class MainPage(BasePage):
    def __init__(self, driver, base_url=None):
        super().__init__(driver, base_url)
        self.driver.implicitly_wait(10)
        self._status_code = By.XPATH, '//span[contains(@class, "response-code")]'
        self._response_body = By.XPATH, '//pre[contains(@data-key, "output-response") and not(contains(@hidden,"true"))]'

    def get_ui_status_code(self) -> int:
        return int(self.driver.find_element(*self._status_code).text)

    def request_ui_click(self, api, method, description):
        self.driver.find_element(By.XPATH, f'//li[@data-http="{method}" and ./a[@href="{api}" and contains(.,"{description}")]]').click()

    def get_ui_response(self) -> dict:
        return ast.literal_eval(self.driver.find_element(*self._response_body).text or "{'empty': 1}")

    def send_request(self, api, method='get', data=None):
        return getattr(requests, method)(url=self.BASE_URL + api, data=data)

    @staticmethod
    def get_resource(file_name):
        resource_path = os.path.dirname(__file__) + '\\..\\resources\\responses'

        with open(f'{resource_path}\\{file_name}') as f:
            request = json.load(f)

        return request
