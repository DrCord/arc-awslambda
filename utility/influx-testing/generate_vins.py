import json
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


jdata = []
for x in range(10000):
    jdata.append({"vin": id_generator()})
print(json.dumps(jdata))
