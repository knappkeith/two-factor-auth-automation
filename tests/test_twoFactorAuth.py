import pytest
import time
import pyotp
from src.SeleniumWrapper.common import web_element
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="session")
def comcast_config(config_json):
    return config_json['comcast']


@pytest.fixture(scope="session")
def sfdc_config(config_json):
    return config_json['sfdc']


@pytest.fixture(scope="session")
def trello_config(config_json):
    return config_json['trello']


def print_and_sleep(print_str, sleep_time=1):
    print("    - {}".format(print_str))
    time.sleep(sleep_time)


@pytest.mark.sfdc
def test_sfdc_login(browser, twilio_session, sfdc_config):

    # Go to login page
    print(" ")
    print_and_sleep("Navigate to Login Page: '{}'".format(sfdc_config['url']))
    browser.get(sfdc_config['url'])

    # Enter username and password
    print_and_sleep("Enter user name")
    web_element(browser, ('id', 'username')).send_keys(
        sfdc_config['username'])
    print_and_sleep("Enter password + ENTER")
    web_element(browser, ('id', 'password')).send_keys(
        sfdc_config["password"] + Keys.ENTER)

    # Wait for the Verification Field to show
    print_and_sleep("Wait for code to be sent....")
    code_field = web_element(browser, ('id', 'smc'))

    # Get messages from Twilio
    print_and_sleep("GET /messages from Twilio")
    r = twilio_session.get(url_path='Messages')

    # Parse out the code from the message
    print_and_sleep("Parse out code from SMS message")
    code = r.json()['messages'][0]['body'].split(" ")[1]
    print_and_sleep("My Code is: '{}'".format(code))

    # Enter Code
    print_and_sleep("Enter code + ENTER")
    code_field.send_keys(code + Keys.ENTER)

    # Sleep so we can see
    print_and_sleep("Wait so we can see site load", 10)

    # Get an element that exists on login page to assert success
    print_and_sleep("Ensure site is loaded by looking for Logo")
    print_and_sleep("Current site URL is: '{}'".format(browser.current_url))
    proof = web_element(browser, ('id', 'auraAppcacheProgress'))
    assert proof is not None


@pytest.mark.comcast
def test_comcast_login(browser, mailosaur_session, comcast_config):

    # Navigate to URL
    print(" ")
    print_and_sleep("Navigate to Login URL: '{}'".format(
        comcast_config['url']))
    browser.get(comcast_config['url'])

    # Enter User Name and Password
    print_and_sleep("Enter username")
    web_element(browser, ('id', 'user')).send_keys(comcast_config['username'])
    print_and_sleep("Enter password + ENTER")
    web_element(browser, ('id', 'passwd')).send_keys(
        comcast_config['password'] + Keys.ENTER)

    # Get SMS and parse
    print_and_sleep("Click to receive email instead of sms")
    web_element(browser, ('name', 'email_code')).click()
    print_and_sleep("Wait for email from Comacst")
    message = mailosaur_session.wait_for_message(
        search_to=comcast_config['mailosaur.search_str'])['text']['body']
    print_and_sleep("Parse out the Code")
    msg_lines = [x for x in message.split("\r\n") if x != ""]
    for line in msg_lines:
        try:
            code = int(line)
            break
        except Exception:
            pass
    print_and_sleep("My Code is: '{}'".format(str(code)))

    # Enter Code
    print_and_sleep("Enter Code + ENTER")
    web_element(browser, ('id', 'verificationCode')).send_keys(
        str(code) + Keys.ENTER)
    print_and_sleep("Wait so we can see the site load", 15)

    # Verify
    print_and_sleep("Ensure site is loaded by looking for Account Drop Down")
    proof = web_element(browser,
                        ('class name',
                         'xc-header--signin-container--authenticated'))
    print_and_sleep("Current site URL is: '{}'".format(browser.current_url))
    assert proof is not None


@pytest.mark.trello
def test_auth_test(browser, trello_config):

    # Navigate to URL
    print(" ")
    print_and_sleep("Navigate to Login URL: '{}'".format(trello_config['url']))
    browser.get(trello_config['url'])

    # Enter User Name and Password
    print_and_sleep("Enter username")
    web_element(browser, ('id', 'user')).send_keys(trello_config['username'])
    print_and_sleep("Enter password + ENTER")
    web_element(browser, ('id', 'password')).send_keys(
        trello_config['password'] + Keys.ENTER)

    # Start the OTP
    print_and_sleep("Start up the One-Time Time-Based Password Generator")
    totp = pyotp.TOTP(trello_config['auth_app_secret'])
    print_and_sleep("Get current Code")
    code = totp.now()
    print_and_sleep("My Code is: '{}'".format(str(code)))
    print_and_sleep("Enter Code + ENTER")
    web_element(browser, ('id', 'totp')).send_keys(code + Keys.ENTER)

    # Verify
    print_and_sleep("Ensure site is loaded by looking for Account Drop Down")
    print_and_sleep(
        "Current site URL is: '{}'".format(browser.current_url), 10)
    if trello_config['verify_element_id'] != "":
        proof = web_element(browser,
                            ('id', trello_config['verify_element_id']))
        assert proof is not None
