import requests
from src.RequestSession.TestRequests import TestingRequestSession


class TwilioSession(TestingRequestSession):
    def __init__(self, account_sid, auth_token, verify_SSL=True):
        super().__init__()

        # Set whether to verify the SSL cert
        self.verify = verify_SSL

        # Set account info
        self.account_sid = account_sid
        self.auth_token = auth_token

        # Set auth
        self.auth = requests.auth.HTTPBasicAuth(self.account_sid,
                                                self.auth_token)

        # Set base_url
        self.base_url = "https://api.twilio.com/2010-04-01/Accounts/"

    def _build_url(self, url_path, **kwargs):
        '''Return the Full URL to be used based on the specific
        use case of this object
        '''

        return "{base}{sid}/{url_path}.json".format(
            base=self.base_url,
            sid=self.account_sid,
            url_path=url_path)
