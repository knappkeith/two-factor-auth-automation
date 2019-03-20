# two-factor-auth-automation
Code for Slalom QE Summit 2019: 2-Factor Authentication


## Install

**Note** only tested out on Mac.

```bash
$ git clone git@github.com:knappkeith/two-factor-auth-automation.git
-or-
$ git clone https://github.com/knappkeith/two-factor-auth-automation.git

$ cd two-factor-auth-automation
$ pip install -r requirements.txt
```

You will need to at least have Chrome installed.

## Usage

You will need to set up Mailosaur and Twilio:

* Twilio:
  * [sign-up](https://www.twilio.com/try-twilio)
  * you will get some free money $$$
  * buy a number, cost is $1 / month, receive text ~ $0.007
  * get your Auth Key and SID, Save for later
* Mailosaur:
  * [sign-up](https://mailosaur.com/app/free-trial/)
  * 14 day free trial
  * create a server, save server id for later
  * get your API Key, save for later

For these 'tests' to work you will need to have accounts for the following with the correct type of 2-Factor set up:

* [SFDC](https://www.salesforce.com/form/signup/freetrial-elf-v2/) - SMS (use twilio phone number)
* [Comcast/Xfinity](https://idm.xfinity.com/myaccount/create-uid?execution=e1s1) - Email (I used my personal then forwarded the email to the mailosaur service)
* [Trello](https://trello.com/signup) - Authenticator App (I used a QR reader to read the secret from the QR code, but also put it in Google Authentictor)

Not that I don't like you all but I don't want to give all my creds so you will need to create a creds file.  You can find an example `creds_template.json`

1. Copy the template: `$ cp creds_template.json ~/2fa_creds.json`
1. Edit your copy and enter the needed info
  * `comcast`:
    * `username`: your Comcast User Name
    * `password`: your Comcast Password
    * `mailosaur.search_str`: your Comcast email for 2 factor
  * `sfdc`:
    * `username`: your SFDC User Name
    * `password`: your SFDC Password
  * `trello`:
    * `username`: your Trello User Name
    * `password`: your Trello Password
    * `auth_app_secret`: your secret from the QR code
    * `verify_element_id`: [optional] the id of the element for your avatar img in the upper right corner
1. Set your creds path environment variable:
  * `$ export CREDS_PATH='~/2fa_creds.json'`

To Run all three examples:

```bash
$ pytest --html=reports/report.html -v -s
```

To Run a specific test:

```bash
$ pytest --html=reports/report.html -v -s -m {sfdc/comcast/trello}
```
