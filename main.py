import requests
import hashlib
import base64
from urllib.parse import quote
import time, datetime

from twilio.rest import Client

print(str(round(time.time())))

# Request parameter test
method = 'GET'
url = 'saas.cleargrass.com'
sub_url = '/v2/device/pheasant/data/fc/'
device_id = '761B5379295BA4BE6EA232E4DB029D43'
# start = str(round(time.time()-86400))
# end = str(round(time.time()))
print('')
start = str(1572883200)
end = str(1572991200)
offset = '0'
limit = '50'
timestamp = '0.111'
token = '0bd48fd37ee444029d499a94470461fc'
asc = 'false'
key = 'ff3f2801c8d942b484431fcd386f5463'

# Init key signature parameter
value = '{}?{}?{}{}&asc={}&end={}&limit={}&offset={}&start={}&timestamp={}&token={}&key={}'.\
    format(method, url, sub_url, device_id, asc, end, limit, offset, start,timestamp, token, key)

# encode init key by sha256 -> base64 -> url_encode -> UpperCase
sha256_encode = hashlib.sha256(value.encode('utf-8')).digest()
base64_encode = base64.b64encode(sha256_encode)
url_encode = quote(base64_encode, 'utf-8')
Key_signature = url_encode.upper()
print(Key_signature)

# Request url
url = 'https://{}{}{}?asc={}&device_id={}&end={}&key={}&limit={}&offset={}&start={}&timestamp={}&token={}'\
    .format(url, sub_url, device_id, asc, device_id, end, Key_signature, limit, offset,start, timestamp, token)

r=requests.get(url)

print("status code:",r.status_code)
print("Headers:",r.headers)

response_dict=r.json()
print("Total repositories:",response_dict)

# trans data timestamp to formal time
ts = response_dict['data']['data'][0]['timestamp']

# catch special data
_temperature = response_dict['data']['data'][0]['temperature']
_humidity = response_dict['data']['data'][0]['humidity']
_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))

print(_time)


# Sending text to phone
def sendMessage(toPhoneNumber, Msg):
    ac_sid = 'AC503ca45a9ce0d4c1d546860e7129274f'

    ac_sid_ap = 'A6461D1B394EBD0169FCD77AD777F11B'
    auth_token = 'cd2e8835cc3fbb8a6aace5e77489bcb4'

    client = Client(ac_sid_ap, auth_token)

    message = client.messages.create(
        to = '+86' + toPhoneNumber,
        from_ = '+12054489135',
        body = Msg
    )

    print(message.sid)

# Msg = 'Current temperature is {}, humidity is {}, time is {}!!!!'.format(_temperature, _humidity, _time)
# sendMessage('17817653989', Msg)