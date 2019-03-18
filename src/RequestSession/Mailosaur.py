from src.RequestSession.TestRequests import TestingRequestSession


class MailosaurSession(TestingRequestSession):
    def __init__(self, api_key, server_id, verify_SSL=True):

        super().__init__()
        self.verify = verify_SSL
        self.base_url = "https://mailosaur.com/api"
        self.auth = (api_key, '')
        self.server_id = server_id
        self.params = {"server": self.server_id}

    def _build_url(self, url_path):
        return "{}/{}".format(self.base_url, url_path)

    def search_for_message(self, search_to=None, search_subject=None,
                           search_body=None, override_server_id=None,
                           **kwargs):
        if override_server_id is not None:
            server_id = override_server_id
        else:
            server_id = self.server_id
        post_body = {
            "sentTo": search_to,
            "subject": search_subject,
            "body": search_body
        }
        if "params" in kwargs.keys():
            kwargs['params']['server'] = server_id
        else:
            kwargs['params'] = {'server': server_id}
        r = self._send_request(
            method='post',
            url_path='messages/search',
            json=post_body, **kwargs)
        if r.status_code != 200:
            raise Exception
        return r

    def wait_for_message(self,
                         search_to=None, search_subject=None, search_body=None,
                         timeout=300, override_server_id=None, **kwargs):
        if override_server_id is not None:
            server_id = override_server_id
        else:
            server_id = self.server_id
        post_body = {
            "sentTo": search_to,
            "subject": search_subject,
            "body": search_body
        }
        if "params" in kwargs.keys():
            kwargs['params']['server'] = server_id
        else:
            kwargs['params'] = {'server': server_id}
        r = self._send_request(
            method='post',
            url_path='messages/await',
            json=post_body,
            timeout=timeout, **kwargs)
        if r.status_code != 200:
            raise Exception
        return r.json()
