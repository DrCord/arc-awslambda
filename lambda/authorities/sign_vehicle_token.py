import logging
import sys
import json
import base64
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

import authorities

# crypto support
sys.path.append('./cryptography')
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True
    },
    'token': {
        'type': 'dict',
        'required': True
    }
})

SIGNATURE_DELIMITER = '\n====SIGNATURE====\n'


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.vehicle.sign')
def sign_vehicle_token(id, token):
    global logger

    vin = token.get('vin', None)
    if not vin:
        raise ArcimotoArgumentError('vin must be present in token')

    cursor = arcimoto.db.get_cursor()
    authorities_resources = authorities.Authorities()

    # look up the authority id
    query = (
        'SELECT encrypted_private_key '
        'FROM authority_keys '
        'WHERE authority_keys_id=%s'
    )
    cursor.execute(query, [id])
    authority_record = cursor.fetchone()
    if authority_record is None:
        raise ArcimotoNotFoundError('No matching authority found')
    encrypted_private_key = authority_record[0]

    if authorities_resources.vehicle_exists(vin) is False:
        raise ArcimotoNotFoundError('vin does not exist')

    if authorities_resources.authority_has_authority_for_vin(id, vin) is False:
        raise ArcimotoArgumentError('Authority id does not control vin')

    # initialize kms client
    client = boto3.client('kms')
    # decrypt our private key with KMS
    decrypt_response = client.decrypt(
        CiphertextBlob=bytes(encrypted_private_key)
    )
    decrypted_private_key = decrypt_response['Plaintext']

    # load private key
    private_key = load_pem_private_key(
        decrypted_private_key,
        password=None,
        backend=default_backend()
    )

    # flatten the token data
    key_data_string = json.dumps(token).encode('utf-8')

    # generate the signature
    signature = private_key.sign(
        key_data_string,
        ec.ECDSA(hashes.SHA256())
    )
    (r, s) = utils.decode_dss_signature(signature)
    signature_b64 = base64.b64encode(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))

    # concatenate the key data, delimiter and signature to make a key slug
    signed_key_data = key_data_string.decode('utf-8') + SIGNATURE_DELIMITER + signature_b64.decode('utf-8')

    return {'token': signed_key_data}


lambda_handler = sign_vehicle_token
