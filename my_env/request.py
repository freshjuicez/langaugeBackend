import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
url = "http://localhost:5000/tokenize"
data = {"text": "お寿司が食べたい。"}
response = requests.post(url, json=data, timeout=10)  # 10 seconds timeout
print(response.json())