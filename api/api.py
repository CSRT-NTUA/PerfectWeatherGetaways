# DO NOT RUN ALL THE TIME
# WE HAVE QUOTAS
import requests
import openai
import json 
import os

openai.api_key = "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"
def get_answer(prompt:str, categories = []):
  # response 
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "user",
        "content": prompt,
      },
    ],
    response_format={ "type": "json_object" },
    max_tokens=3000,
  )
  # get the results of the api, it's in json format 
  response = response["choices"][0]["message"]["content"]
  json_result = json.loads(response)
  json_places = None
  if json_result.get('places'):
    json_places = json_result['places']
  res = []
  for x in json_places:
    res.append(travelmyth_api(x, categories))
  return res

def travelmyth_api(destination, categories):
  url = "https://www.travelmyth.gr/api_chat_makeathon.php"
  params = {
      "destination": destination,
      "lang": "en",
      "categories": categories,
      "apiKey": "csrt"
  }
  headers = {"content-type": "application/json"}
  
  response = requests.get(url, params=params, headers=headers)
  
  if response.status_code == 200:
      data = response.json()
      return data
      # Process the JSON data here
  else:
      print("Error:", response.status_code)

