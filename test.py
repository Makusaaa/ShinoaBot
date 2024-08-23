import requests
import json

body = {
  "pageSize": 200
}
response = requests.post('https://api.gms.moontontech.com/api/gms/source/2669606/2681577', json=body)
data = json.loads(response.text)

for d in data['data']['records']:
  print(d['data']['name'])