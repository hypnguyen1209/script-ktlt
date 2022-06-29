import argparse
from urllib.parse import urlparse
import sys
import subprocess
import json


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


parser = argparse.ArgumentParser(
    description='Script identifies technologies on websites')
parser.add_argument('--url', help='URL argument', required=True)
args = parser.parse_args()
url = args.url

if not url_validator(url):
    print('[+] URL invalid')
    sys.exit()

proc = subprocess.Popen(['node', 'wappalyzer/src/drivers/npm/cli.js',
                        url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()
result = json.loads(out)
status = result['urls'][url]['status']
techs = result['technologies']
print(f"[+] URL: {url}")
print(f"[+] Status: {status}")
print('[+] Technologies: ')
for item in techs:
    name = item['name']
    ver = ' ('+item['version']+')' if item['version'] else ''
    for cate in item['categories']:
        name_cate = cate['name']
        print(f"[-] {name_cate} - {name}{ver}")
