import logging
import sys
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

# crypto support
sys.path.append('./cryptography')
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.authority.re-key')
@arcimoto.db.transaction
def rekey_authority(id):
    global logger

    cursor = arcimoto.db.get_cursor()

    # Fetch the current authority record for the kms key and to validate the id
    query = (
        'SELECT cmk_id '
        'FROM authority_keys '
        'WHERE authority_keys_id=%s'
    )
    cursor.execute(query, [id])
    if cursor.rowcount != 1:
        raise ArcimotoArgumentError('rekey_authority check did not match exactly one authority')

    row = cursor.fetchone()

    cmk_id = row[0]

    # generate key pair and get PEM encoded byte representations
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    # initialize kms client
    client = boto3.client('kms')
    encrypt_response = client.encrypt(
        KeyId=cmk_id,
        Plaintext=private_key_bytes
    )
    encrypted_private_key = encrypt_response['CiphertextBlob']

    # update the authority store with the new keys
    query = (
        'UPDATE authority_keys '
        'SET public_key=%s, encrypted_private_key=%s '
        'WHERE authority_keys_id=%s'
    )
    cursor.execute(
        query,
        [
            bytearray(public_key_bytes),
            bytearray(encrypted_private_key),
            id
        ]
    )
    if cursor.rowcount != 1:
        raise ArcimotoException('rekey_authority update did not match exactly one authority')

    return {}


lambda_handler = rekey_authority
