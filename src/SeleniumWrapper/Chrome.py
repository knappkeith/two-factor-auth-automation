from selenium import webdriver
from src.SeleniumWrapper.common import get_executable_path


class Selenium_Wrapper_Chrome(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        self.browser_name = 'Chrome'

        # Get executable path
        kwargs = get_executable_path(kwargs, "chromedriver")

        # Set up Selenium Driver
        super(Selenium_Wrapper_Chrome, self).__init__(*args, **kwargs)

    @property
    def version(self):
        return self.create_options().to_capabilities()
