# The following code is heavily adapted from the python example generated by
# the Victorian State Government Department of Transport/VicRoads API website:
# https://data-exchange-test.vicroads.vic.gov.au/api-details#api=srods-disruptions-road-apiv1&operation=get-planneddisruptions

import requests, json

url = "https://data-exchange-test-api.vicroads.vic.gov.au/opendata/disruptions/v1/planned?format=GeoJson"

# Request headers
header = {'Cache-Control': 'no-cache'}
header_secrets = json.load(open("secrets.json"))
header.update(header_secrets)

data = requests.get(url, headers=header).json()
print(data)
