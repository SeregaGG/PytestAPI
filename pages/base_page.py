
class BasePage:
    BASE_URL: str = "https://reqres.in"
    driver = None

    def __init__(self, driver, base_url=None):
        if not base_url is None:
            self.BASE_URL = base_url
        self.driver = driver
        self.driver.get(self.BASE_URL)
