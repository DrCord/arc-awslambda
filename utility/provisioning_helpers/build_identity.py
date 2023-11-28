import argparse
import json
import getpass

AWS_ROOT = "AmazonRootCA4"
AWS_ENDPOINT = "a3pzb3h0tgvmya.iot.us-west-2.amazonaws.com"


parser = argparse.ArgumentParser(description='build vehicle identity.json file from AWS artifacts')
parser.add_argument('vin', help='VIN identifying vehicle identity')
parser.add_argument('--pretty', action='store_true', help='pretty print output JSON', default=False)
parser.add_argument('--root', help='the AWS root certificate to use', default=AWS_ROOT)
parser.add_argument('--endpoint', help='the IoT endpoint to use', default=AWS_ENDPOINT)
parser.add_argument('--cert', help='the client certificate')
parser.add_argument('--key', help='the client certificate key')
parser.add_argument('--pin', help='the factory PIN')
parser.add_argument('--no-heated-seats', dest='heated_seats', action='store_false', help='heated seats option enabled', default=True)
parser.add_argument('--no-heated-grips', dest='heated_grips', action='store_false', help='heated grips option enabled', default=True)
parser.add_argument('--no-stereo-enabled', dest='stereo_enabled', action='store_false', help='stereo installed option', default=True)


args = parser.parse_args()

pin = ''
if args.pin is None:
    while len(pin) != 6:
        pin = getpass.getpass("PIN is requried: ")
        try:
            pin_int = int(pin)
        except ValueError as e:
            pin = ''
else:
    pin = args.pin

identity = {
    'vin': args.vin,
    'aws_endpoint': args.endpoint,
    'pin': pin,
    'options': {
        'heated_seats': args.heated_seats,
        'heated_grips': args.heated_grips,
        'stereo_enabled': args.stereo_enabled
    }
}

with open(args.cert) as cert:
    identity['client_cert'] = cert.read()

with open(args.key) as key:
    identity['client_key'] = key.read()

with open(args.root) as ca:
    identity['aws_cert'] = ca.read()

if args.pretty:
    print(json.dumps(identity, indent=2))
else:
    print(json.dumps(identity))
