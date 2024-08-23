import requests
import base64

link = 'aHR0cHM6Ly9oYWhvLm1vZQ=='
test = base64.b64decode(link)
print(requests.get(test).text)