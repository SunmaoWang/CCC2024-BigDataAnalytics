# The following code is heavily adapted from the python example from the "PTV 
# Timetable API – API Key and Signature information" document, avaliable at:
# https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/

from hashlib import sha1
import hmac
def getUrl(request):
    devId = 2
    key = b'7car2d2b-7527-14e1-8975-06cf1059afe0'
    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw.encode('utf-8'), sha1)
    signature = hashed.hexdigest()
    return 'http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)

print(getUrl('/v3/disruptions'))
