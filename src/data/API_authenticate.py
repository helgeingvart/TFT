import requests
import json

reqUrl = "https://kystdatahuset.no/ws/api/auth/login"

headersList = {
 "User-Agent": "Your Client (https://your-client.com)",
 "accept": "*/*",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "username": "",
  "password": """"""
})

response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

print(response.text)