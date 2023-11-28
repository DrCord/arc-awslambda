import json
import argparse

parser = argparse.ArgumentParser(description='split provision API response into individual useful files')
parser.add_argument('file', help='the file containing the API response JSON')

args = parser.parse_args()


with open(args.file) as f:
	data = json.load(f)

vin = data['vin']

certificate = data['certificate']
with open("{}.crt".format(vin), "w") as f:
	f.write(certificate)

private_key = data['private_key']
with open("{}.key".format(vin), "w") as f:
	f.write(private_key)