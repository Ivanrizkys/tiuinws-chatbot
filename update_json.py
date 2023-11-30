import json
import requests

import config

res = requests.get('https://chatbot-dashboard.fly.dev/api/intents?sort=id&pagination[pageSize]=100', headers=config.HEADERS)
res_data = res.json()['data']

json_data = json.dumps(res_data, indent=2)
with open("data.json", "w") as outfile:
    outfile.write(json_data)

print("Update JSON File Sucesfully")