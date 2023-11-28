import json
import argparse

parser = argparse.ArgumentParser(description='split identity.json into individual useful files')
parser.add_argument('file', help='the file containing the identity')

args = parser.parse_args()


with open(args.file) as f:
	data = json.load(f)

vin = data['vin']

certificate = data['client_cert']
with open("{}.crt".format(vin), "w") as f:
	f.write(certificate)

private_key = data['client_key']
with open("{}.key".format(vin), "w") as f:
	f.write(private_key)
