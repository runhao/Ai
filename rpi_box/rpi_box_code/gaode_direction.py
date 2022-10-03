import json
import requests

key = "a4bd20595b6e9ea56857fa9d7d114b33"

def gaode_direction(origin, destination):
    url = f'https://restapi.amap.com/v3/direction/walking?origin={origin}&destination={destination}&key={key}'
    res = requests.get(url)
    direction = []
    for i in json.loads(res.text)["route"]["paths"][0]["steps"]:
        direction.append(i)
    return direction
