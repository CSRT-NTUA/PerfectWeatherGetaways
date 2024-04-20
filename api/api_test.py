# DO NOT RUN ALL THE TIME
# WE HAVE QUOTAS
import requests
import openai
import json 

def get_answer(prompt:str):
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
  print(response)
  return response["choices"][0]["message"]["content"]

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

prompt = "I want to go for sunny holidays in Europe. I want a city with a big cathedral. Use the following instructions when answering the prompt above: Reply in Json format Include the places suggestions in an array. Suggest as many as you can, preferably at least 10. When writing, the place name includes only the name, not the country, wider region or continent. If the prompt is appropriate for any of the following categories include the category in the json: Categories: infinity_pool,heated_pool,indoor_pool,rooftop_pool,wave_pool,children_pool,panoramic_view_pool,pool_swim_up_bar,pool_water_slide,pool_lap_lanes,water_park,lazy_river,private_pool,dog_play_area,dog_sitting,dogs_stay_free,outdoor_pool,health_and_safety,treehouse,haunted,overwater_bungalows,three_star,skyscraper,four_star,five_star,yoga,tennis,small,adult_only,gym,accessible,cheap,parking,business,free_wifi,pool,nightlife,romantic,dog_friendly,family,spa,casino,honeymoon,eco_friendly,beach,beachfront,ski,ski_in_ski_out,historic,unusual,vineyard,monastery,castle,golf,luxury,boutique,ev_charging,jacuzzi_hot_tub,fireplace,all_inclusive"
response = get_answer(prompt)
json_places = json.loads(response)
print(json_places['places'])
for x in json_places['places']:
  print(travelmyth_api(x, []))
#for x in json_data:
#  print(travelmyth_api(x, []))