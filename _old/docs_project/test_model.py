import requests

url = "http://localhost:11435/api/generate"
data = {"model": "mistral", "prompt": "What is the meaning of life?"}

response = requests.post(url, json=data)
print(response.json()['response'])