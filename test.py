import requests
import datetime
import json

app_id = ""
headers = {"accept": "application/json"}

viimane_nädal = []

for i in range(0,7):
    today = datetime.date.today()
    ago = today - datetime.timedelta(days=i)
    viimane_nädal.append(ago)

viimane_nädal.reverse()
print(viimane_nädal[0])
rates = []
"""
for päev in viimane_nädal:
    url = f"https://openexchangerates.org/api/historical/{päev}.json?app_id={app_id}"
    response = requests.get(url, headers=headers)
    response = response.text
    result = json.loads(response)
    result = result["rates"]
    rates.append(result["EUR"])

print(rates)
"""
