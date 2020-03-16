import requests
from random import randint
import time


headers = {
    'content-type': 'application/vnd.kafka.json.v2+json',
}

for _ in range(50):

    time.sleep(1)
    value = str(randint(0,100))
    data = '{"records":[{"key":"key1", "value":' + '"{}"'.format(value) + '}]}'

    response = requests.post('http://my-bridge.io/topics/my-topic', headers=headers, data=data)


    print(response.text)
