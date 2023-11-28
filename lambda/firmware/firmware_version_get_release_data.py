import base64
import json
import logging
import certifi
import urllib3

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

import firmware

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'repo': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
def firmware_version_get_release_data(repo):
    '''Gets data for each item in the provided Repo, excludes pipeline and readme files '''
    data = {}
    firmware_resources = firmware.Firmware()

    # recommended to do ssl verification for requests
    # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )

    # gets list of files in repo
    api_call_headers = firmware_resources.bb_api_call_headers
    env = arcimoto.runtime.get_env()
    if env is arcimoto.runtime.ENV_PROD:
        branch = 'master'
    else:
        branch = env
    api_call_response = http.request(
        'GET',
        f'{firmware_resources.REQUEST_URL}{repo}/src/{branch}/?pagelen=100',
        headers=api_call_headers
    )
    json_response = json.loads(api_call_response.data.decode('utf-8'))

    # get most recent commit to repo
    entry = firmware_resources.get_commit_info(firmware_resources.bb_token, repo)
    entry['name'] = 'Deployed Firmware'
    data['Repository'] = entry
    for file in json_response['values']:
        # Get the latest commit for each file in the repo
        try:
            filename = file['path']
            # skip `Charger Firmware` file (see TEL-1393, TEL-1394)
            if filename == 'Charger Firmware.BIN':
                continue
            # skip readme and pipeline files
            if filename.split('.')[-1] not in ['md', 'yml']:
                entry = firmware_resources.get_commit_info(firmware_resources.bb_token, repo, filename)
                # special case since this firmware increments name each commit
                if filename.startswith('TAUSYS_SY_AM2.'):
                    filename = 'TAUSYS_SY_AM2.'
                entry['filename'] = filename
                entry['name'] = firmware_resources.FIRMWARE.get(filename, filename.split('.')[0].title())
                data[filename] = entry
        except Exception as e:
            logger.warning('unable to get commit hash for {}: {}'.format(filename, e))

    return {'firmware': data}


lambda_handler = firmware_version_get_release_data
