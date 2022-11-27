import requests
import threading
from time import sleep

def req():
    url     = 'http://localhost:6000'
    payload = { 'key' : 'val' }
    headers = {}
    res = requests.get(url, data=payload, headers=headers)

for i in range(30):
    threading.Thread(target = req).start()
    sleep(2)