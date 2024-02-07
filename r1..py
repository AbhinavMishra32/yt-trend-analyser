# pip install requests
import requests
import json

url = 'https://youtube.com'
apikey = '59ce41315764569232d4828cc347b7c10a31c994'
params = {
    'url': url,
    'apikey': apikey,
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
a = json.dumps(response.text)
print(json.loads(a, indent=4))