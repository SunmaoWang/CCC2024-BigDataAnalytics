# The following code is heavily adapted from the python example from the "PTV 
# Timetable API – API Key and Signature information" document, avaliable at:
# https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/

from hashlib import sha1
import hmac, config

def main():

    devId = config('PTV_DEVID')
    key = str.encode(config('PTV_KEY'))

    all_data = []

    for disrupt_type in ["planned", "current"]:

        request = '/v3/disruptions?'

        if disrupt_type == "planned":
            request += "disruption_status=planned&"
        else:
            request += "disruption_status=current&"
        raw = request+'devid={0}'.format(devId)

        hashed = hmac.new(key, raw.encode('utf-8'), sha1)
        signature = hashed.hexdigest()

        all_data.append('http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature))

    return all_data
