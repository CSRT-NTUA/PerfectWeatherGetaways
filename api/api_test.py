# DO NOT RUN ALL THE TIME
# WE HAVE QUOTAS

import requests
import openai

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "Hello there, can you say hi to me?"
    }
  ],
  temperature=0,
  max_tokens=1000,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
# response["choices"][0]["message"]["content"]
print(response)

url = "https://www.travelmyth.gr/api_chat_makeathon.php"
params = {
    "destination": "Greece",
    "lang": "en",
    "categories": "ski,luxury",
    "apiKey": "csrt"
}
headers = {"content-type": "application/json"}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
    # Process the JSON data here
else:
    print("Error:", response.status_code)
