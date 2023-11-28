import json
import logging
import certifi
import urllib3

from arcimoto.exceptions import *
from distutils.version import StrictVersion
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Bitbucket:

    TOKEN_URL = "https://bitbucket.org/site/oauth2/access_token"
    REQUEST_URL = "https://api.bitbucket.org/2.0/repositories/arcimotocode1/"

    bitbucket_access_token = None
    secret_name = None

    @property
    def bb_token(self):
        return self.bitbucket_access_token if self.bitbucket_access_token is not None else self.get_auth_token()

    @property
    def bb_api_call_headers(self):
        return {'Authorization': 'Bearer ' + self.bb_token}

    def __init__(self, secret_name):
        super().__init__()
        if secret_name is not None:
            self.secret_name = secret_name
        else:
            raise ArcimotoException('Cannot instanstiate Bitbucket class without secret_name')

    def get_auth_token(self):
        """Get OAuth2 token for bitbucket using consumer key and password"""
        credentials = arcimoto.runtime.get_secret(self.secret_name)
        data = {
            'grant_type': 'client_credentials'
        }
        credentials_string = credentials['key'] + ':' + credentials['secret']
        headers = urllib3.make_headers(basic_auth=credentials_string)

        # recommended to do ssl verification for requests
        # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        access_token_response = http.request(
            'POST',
            self.TOKEN_URL,
            fields=data,
            headers=headers
        )
        json_response = json.loads(access_token_response.data.decode('utf-8'))
        self.bitbucket_access_token = json_response.get('access_token', None)

        return json_response.get('access_token', None)

    def get_commit_info(self, token, repo, request_path_parameter=None, use_env=True):
        """Get info for latest commit of ENV branch of provided repo name and request path in ArcimotoCode"""

        api_call_headers = {'Authorization': 'Bearer ' + token}

        try:
            if not use_env:
                branch = 'master'
            else:
                env = arcimoto.runtime.get_env()
                if env is arcimoto.runtime.ENV_PROD:
                    branch = 'master'
                else:
                    branch = env

            request_path = f'{self.REQUEST_URL}{repo}/commits/{branch}'

            if request_path_parameter:
                request_path += '?'
                request_path += f'path={request_path_parameter.replace(" ", "%20")}'
        except Exception as e:
            raise ArcimotoException(f'Unable to create request_path: error: {e}') from e

        try:
            # recommended to do ssl verification for requests
            # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
            http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
            api_call_response = http.request(
                'GET',
                request_path,
                headers=api_call_headers
            )
        except Exception as e:
            raise ArcimotoException(f'Unable to complete urllib3 http GET request for commit info - error: {e}') from e

        try:
            json_response = json.loads(api_call_response.data.decode('utf-8'))
            json_response_list = json_response.get('values', [])
            json_response_item = json_response_list[0] if len(json_response_list) else {}
        except Exception as e:
            raise ArcimotoException(f'Unable to parse json response - error: {e}') from e

        return {
            'hash': json_response_item.get('hash', ''),
            'author': json_response_item.get('author', {}).get('raw', ''),
            'date': json_response_item.get('date', ''),
            'message': json_response_item.get('message', '').replace('\n', '')
        }

    def get_latest_tag_name(self, token, repo):
        """Gets the latest tag for a given repo"""

        api_call_headers = {'Authorization': 'Bearer ' + token}

        try:
            request_path = f'{self.REQUEST_URL}{repo}/refs/tags?pagelen=1&sort=-target.date&fields=values.name'

        except Exception as e:
            raise ArcimotoException(f'Unable to create request_path: error: {e}') from e

        try:
            # recommended to do ssl verification for requests
            # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
            http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
            api_call_response = http.request(
                'GET',
                request_path,
                headers=api_call_headers
            )
        except Exception as e:
            raise ArcimotoException(f'Unable to complete urllib3 http GET request for commit info - error: {e}') from e

        try:
            json_response = json.loads(api_call_response.data.decode('utf-8'))
            json_response_list = json_response.get('values', [])
            json_response_item = json_response_list[0] if len(json_response_list) else {}
            version_number = json_response_item.get('name', '')[1:]
        except Exception as e:
            raise ArcimotoException(f'Unable to parse json response - error: {e}') from e

        return {
            'latest_version': version_number
        }
