import requests
import json
import pandas as pd
#from pandas.io.json import json_normalize

urlheader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "authority": "www.nseindia.com",
    "scheme":"https"
}

expiry_dt = '27-Oct-2022'
url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
data = requests.get(url, headers=urlheader).content
data2 = data.decode('utf-8')
df = json.loads(data2)
json_ce = eval("[data['CE'] for data in df['records']['data'] if 'CE' in data and data['expiryDate'] == '" + expiry_dt + "']")
#df_ce = json_normalize(json_ce)
#print('*** NIFTY Call Options Data with Expiry Date: '+ expiry_dt + ' *** \n', df_ce)
json_pe = eval("[data['CE'] for data in df['records']['data'] if 'PE' in data and data['expiryDate'] == '" + expiry_dt + "']")
#df_pe = json_normalize(json_pe)
#print('*** NIFTY Put Options Data with Expiry Date: '+ expiry_dt + ' *** \n', df_pe)



json_object = json.loads(data2)
json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)
#print(json_ce)
