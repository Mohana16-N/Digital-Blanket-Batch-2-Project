import requests

url = "http://127.0.0.1:5000/optimize"
data = {"room_temp": 24, "outside_temp": 30, "energy": 40}

response = requests.post(url, json=data)
print("Response:", response.json())
