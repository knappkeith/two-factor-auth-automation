from selenium import webdriver
from src.SeleniumWrapper.common import get_executable_path


class Selenium_Wrapper_Firefox(webdriver.Firefox):
    def __init__(self, *args, **kwargs):
        self.browser_name = 'Firefox'

        # Get executable path
        kwargs = get_executable_path(kwargs, "geckodriver")

        # Set up Selenium Driver
        super(Selenium_Wrapper_Firefox, self).__init__(*args, **kwargs)

    @property
    def version(self):
        return self.create_options().to_capabilities()
