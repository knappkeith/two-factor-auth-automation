import sys
import os
sys.path.append(os.path.split(os.path.dirname(__file__))[0])

import pytest
from src.RequestSession.Twilio import TwilioSession
from src.RequestSession.Mailosaur import MailosaurSession
from src.SeleniumWrapper.FireFox import Selenium_Wrapper_Firefox
from src.SeleniumWrapper.Chrome import Selenium_Wrapper_Chrome
from src.tools.os_structure import read_json_file
from src.tools.misc import get_environment_variable


###############################################################################
# FIXTURES
###############################################################################
@pytest.fixture(scope='session')
def twilio_session(config_json):
    auth_key = config_json['twilio.authKey']
    twilio_sid = config_json['twilio.sid']
    return TwilioSession(account_sid=twilio_sid, auth_token=auth_key)


@pytest.fixture(scope='session')
def mailosaur_session(config_json):
    server_id = config_json['mailosaur.serverId']
    api_key = config_json['mailosaur.apiKey']
    return MailosaurSession(api_key=api_key, server_id=server_id)


@pytest.fixture(scope="function")
def browser(request):
    """Returns a Selenium Browser Instance, they browser type is set with the
    command line arguement --browser with Chrome being the default.
    """

    driver = get_browser(browser_type=request.config.option.browser)
    yield driver

    try:
        driver.close()
    except Exception as e:
        print(e, " There was an issue closing the broswer!")


@pytest.fixture(scope="session")
def config_json(request):
    return read_json_file(
        get_environment_variable(variable_name="CREDS_PATH",
                                 default="./creds_template.json"))
###############################################################################
# END Fixtures
###############################################################################


###############################################################################
# HOOKS
###############################################################################
def pytest_addoption(parser):
    '''
    Add command line arguements here.
    '''

    # Browser
    parser.addoption(
        "--browser",
        action='store',
        default='chrome',
        help="Specify browser to use.")
###############################################################################
# END HOOKS
###############################################################################


###############################################################################
# FUNCTIONS
###############################################################################
def get_browser(browser_type=None):
    desired_browser = browser_type.upper()
    if desired_browser == 'CHROME':
        # To Make this headless uncomment the following
        # from selenium.webdriver.chrome.options import Options
        # chrome_opts = Options()
        # chrome_opts.add_argument("--headless")
        # chrome_opts.add_argument("--window-size=1920x1080")
        # return Selenium_Wrapper_Chrome(chrome_options=chrome_opts)
        return Selenium_Wrapper_Chrome()
    elif desired_browser == 'FIREFOX':
        return Selenium_Wrapper_Firefox()
###############################################################################
# END FUNCTIONS
###############################################################################
