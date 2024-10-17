import requests as req
import json

url = "https://dog.ceo/api/breeds/image/random?message"

payload = {}
headers = {
    "message" : "5"
}

response = req.request("GET", url, headers=headers, data=payload)

print(response.text)

data = json.loads(response.text)
print(data["message"])