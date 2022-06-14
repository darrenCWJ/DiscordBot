import os
import discord
import requests
import json

client = discord.Client()

def get_location_user():
  ip_stack = os.environ['IPSTACK']
  send_url = "http://api.ipstack.com/check?access_key="+ip_stack
  geo_req = requests.get(send_url)
  geo_json = json.loads(geo_req.text)
  print(geo_json)
  latitude = geo_json['latitude']
  longitude = geo_json['longitude']
  city = geo_json['city']
  return geo_json

# for singapore carparks
def get_carpark_status(carpark_id):
  send_url = "https://api.data.gov.sg/v1/transport/carpark-availability"
  carpark_req = requests.get(send_url)
  carpark_json = json.loads(carpark_req.text)
  carpark_data = carpark_json['items'][0]['carpark_data']
  
  for i in range(len(carpark_data)):
      if carpark_data[i]['carpark_number'] == carpark_id.upper():
          total_lots = carpark_data[i]['carpark_info'][0]['total_lots']
          lots_available = carpark_data[i]['carpark_info'][0]['lots_available']
          return total_lots, lots_available
  return None, None
    

@client.event
async def on_ready():
  print(f"Ready : {client.user}")

@client.event
async def on_message(message):
  msg = message.content
  
  if message.author == client.user:
    return
  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$location_me'):
    geoloc = get_location_user()
    await message.channel.send(f'your location is {geoloc}')

  if msg.startswith('$carpark_slots'):
    try: 
      carparkloc = msg.split()[1]
      carparkloc = carparkloc.strip()
    except:
      await message.channel.send(f"couldn't get ID from message")
      return
    await message.channel.send(f'searching for carpark ID: {carparkloc}')
    total_lots, lots_available = get_carpark_status(carparkloc)
    if not total_lots:
      await message.channel.send(f"not in list of carparks in singapore")
    else:
      await message.channel.send(f'total lots: {total_lots}, available lots: {lots_available}')


client.run(os.environ['TOKEN'])
