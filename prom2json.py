#!/usr/bin/env python3

import json
import sys
try:
    import requests
except ImportError:
    sys.exit("Failed to import requests library, `pip install requests`")

DEVMODE=True

HOSTNAME="localhost"
PORT=40355
if len(sys.argv) == 2:
    HOSTNAME,PORT = sys.argv
elif len(sys.argv) == 1:
    PORT = sys.argv[0]

URL=f"http://{HOSTNAME}:{PORT}/metrics"
print(URL)

if DEVMODE:
    lines = open("data.prom", "r").read().split("\n")
else:
	try:
	   response = requests.get(URL)
	   response.raise_for_status()
	except Exception as error_message:
	   sys.exit(f"Failed to query {URL}, bailing - error: {error_message}")
	lines = response.text.split("\n")

data = {}
for line in lines:
    if not line.startswith("#"):
        linedata = line.split()
        if len(linedata) == 2:
            #print(linedata)
            if "{" not in linedata[0]:
                #print(f"Adding {linedata[0]} : {linedata[1]}", file=sys.stderr)
                data[linedata[0]] = linedata[1]
            else:
                sub_data  = linedata[0].split("{")
                if sub_data[0] not in data:
                    data[sub_data[0]] = {}
                sub_key = sub_data[1]
                for el in ["{", "}", '"']:
                    sub_key = sub_key.replace(el, "")
                final_sub_key = sub_key.replace("=", "_")
                #print(f"Adding: data[{sub_data[0]}][{final_sub_key}] = {linedata[1]}", file=sys.stderr)
                data[sub_data[0]][final_sub_key] = linedata[1]

print(json.dumps(data, indent=2))