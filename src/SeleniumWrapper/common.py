import time
from src.tools import os_structure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def web_element(driver, locator, timeout=10):
    waiter = WebDriverWait(driver, timeout)
    waiter.until(
        lambda driver: driver.find_element(*locator))
    element = driver.find_element(*locator)
    return element


def web_elements(driver, locator, timeout=10):
    web_element(driver=driver, locator=locator, timeout=timeout)
    return driver.find_elements(*locator)


def async_web_elements(driver, locator, timeout=10, polling_interval=1):
    # Get initial elements
    items = web_elements(driver=driver, locator=locator, timeout=timeout)
    prev_cnt = 0

    # Poll until previous count is equal to current count
    while len(items) > prev_cnt:
        prev_cnt = len(items)
        time.sleep(polling_interval)
        items = web_elements(driver=driver, locator=locator, timeout=timeout)

    return items


def check_for_element(driver, locator, timeout=10):
    try:
        element = web_element(driver=driver, locator=locator, timeout=timeout)
        return element
    except TimeoutException:
        return None


def get_executable_path(kwargs, driver_name):
    if kwargs.get("executable_path") is None:
        exe_path = os_structure.find_files(
            "./drivers", "{}*".format(driver_name))
        if len(exe_path) > 0:
            exe_path = exe_path[0]
        else:
            msg = "Unable to find '{}' in /drivers folder!".format(driver_name)
            raise OSError(os_structure._build_error_str(2).format(arg=msg))
        kwargs['executable_path'] = exe_path
    return kwargs


def wait_element_is_clickable(driver, locator, timeout=10):
    waiter = WebDriverWait(driver, timeout)
    waiter.until(EC.element_to_be_clickable(locator))
    element = driver.find_element(*locator)
    return element


def wait_for_new_window(driver, current_window, timeout=10):
    waiter = WebDriverWait(driver, timeout)
    my_window = new_window_handle(current_window)
    waiter.until(my_window)
    return my_window.new_window


def wait_for_url(driver, url_contains, timeout=10):
    '''Will poll until driver.current_url contains the passed string
    '''
    waiter = WebDriverWait(driver, timeout)
    my_url = change_url_handle(url_contains)
    waiter.until(my_url)
    return driver.current_url


class new_window_handle(object):
    def __init__(self, current_window):
        self.current_window = current_window
        self.new_window = None

    def __call__(self, driver):
        for handle in driver.window_handles:
            if handle != self.current_window:
                self.new_window = handle
                return True
        return False


class change_url_handle(object):
    '''Change of url handle used in 'wait_for_url'
    '''
    def __init__(self, url_contains):
        self.url_contains = url_contains

    def __call__(self, driver):
        if self.url_contains in driver.current_url:
            return True
        return False
