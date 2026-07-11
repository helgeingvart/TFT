import requests
import json

reqUrl = "https://kystdatahuset.no/ws/api/auth/login"

headersList = {
 "User-Agent": "Your Client (https://your-client.com)",
 "accept": "*/*",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "username": "helgeingvart@gmail.com",
  "password": """izX!Pa8r3Rka8UE"""
})

response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

print(response.text)