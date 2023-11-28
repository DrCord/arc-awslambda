import json
import argparse

SIGNATURE_DELIMITER = "\n====SIGNATURE====\n"


parser = argparse.ArgumentParser(description='split the token signing API response into a useful signed token')
parser.add_argument('file', help='the file containing the API response JSON')

args = parser.parse_args()

with open(args.file) as f:
	data = json.load(f)

token_string, signature = data['token'].split(SIGNATURE_DELIMITER)
token = json.loads(token_string)
vin = token['vin']

with open("{}.token".format(vin), "w") as f:
	f.write(data['token'])