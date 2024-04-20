import requests
import json
import os
print("in the script")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

url = "https://api.openai.com/v1/chat/completions"
headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {OPENAI_API_KEY}"
}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Say this is a test!"}],
    "max_tokens": 60
}

response = requests.post(url, json=data, headers=headers)
print(response)
print(response.status_code)
try: 
    print(response.json())
    print(response.json()["choices"][0]["message"]["content"])
except Exception as e: 
    print(e)
    # print(response.text)
# completion = response.json()["choices"][0]["text"]
# print("Completion:", completion)