import logging
import boto3
import sys
import json

import arcimoto.db
import arcimoto.user
import arcimoto.args
import arcimoto.runtime
from arcimoto.exceptions import *

import authorities

# crypto support
sys.path.append('./cryptography')
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DEFAULT_KMS_ID = '0e6e6f67-26ba-48cc-9788-4acab6de74bb'
DEFAULT_PARENT_AUTHORITY_ID = 1  # Defaults to a subordinate of Arcimoto

arcimoto.args.register({
    'description': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'parent_authority_id': {
        'type': 'integer',
        'nullable': True,
        'default': DEFAULT_PARENT_AUTHORITY_ID
    },
    'use_default_kms_cmk': {
        'type': 'boolean',
        'nullable': True,
        'default': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.authority.create')
@arcimoto.db.transaction
def create_authority(description, parent_authority_id=DEFAULT_PARENT_AUTHORITY_ID, use_default_kms_cmk=True):
    global logger

    cursor = arcimoto.db.get_cursor()
    authorities_resources = authorities.Authorities()

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

    # a default kms key
    kms_id = DEFAULT_KMS_ID

    if not use_default_kms_cmk:
        create_key_response = client.create_key(
            Policy='''{ "Version": "2012-10-17", "Statement": [ { "Sid": "Enable IAM User Permissions", "Effect": "Allow", "Principal": { "AWS": [ "arn:aws:iam::511596272857:root" ] }, "Action": "kms:*", "Resource": "*" }, { "Sid": "Allow access for Key Administrators", "Effect": "Allow", "Principal": { "AWS": [ "arn:aws:iam::511596272857:role/lambda-vpc-role" ] }, "Action": [ "kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*", "kms:Update*", "kms:Revoke*", "kms:Disable*", "kms:Get*", "kms:Delete*", "kms:TagResource", "kms:UntagResource", "kms:ScheduleKeyDeletion", "kms:CancelKeyDeletion" ], "Resource": "*" }, { "Sid": "Allow use of the key", "Effect": "Allow", "Principal": { "AWS": [ "arn:aws:iam::511596272857:role/lambda-vpc-role" ] }, "Action": [ "kms:Encrypt", "kms:Decrypt", "kms:ReEncrypt*", "kms:GenerateDataKey*", "kms:DescribeKey" ], "Resource": "*" }, { "Sid": "Allow attachment of persistent resources", "Effect": "Allow", "Principal": { "AWS": [ "arn:aws:iam::511596272857:role/lambda-vpc-role" ] }, "Action": [ "kms:CreateGrant", "kms:ListGrants", "kms:RevokeGrant" ], "Resource": "*", "Condition": { "Bool": { "kms:GrantIsForAWSResource": true } } } ] }''',
            Description=description,
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS',
            BypassPolicyLockoutSafetyCheck=False
        )
        kms_id = create_key_response['KeyMetadata']['KeyId']

    # have KMS encrypt the private key
    encrypt_response = client.encrypt(
        KeyId=kms_id,
        Plaintext=private_key_bytes
    )
    encrypted_private_key = encrypt_response['CiphertextBlob']

    if not authorities_resources.authority_exists(parent_authority_id):
        raise ArcimotoNotFoundError('Invalid parent authority id')

    # store a record of everything in the authority_keys table
    query = (
        'INSERT INTO authority_keys '
        '(parent_authority_id, cmk_id, public_key, encrypted_private_key, description) '
        'VALUES (%s, %s, %s, %s, %s) '
        'RETURNING authority_keys_id'
    )
    cursor.execute(query, [parent_authority_id, kms_id, bytearray(public_key_bytes), bytearray(encrypted_private_key), description])

    authority_id = cursor.fetchone()[0]

    return {'id': authority_id}


lambda_handler = create_authority
