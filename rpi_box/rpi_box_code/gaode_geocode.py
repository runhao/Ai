import requests

key = "a4bd20595b6e9ea56857fa9d7d114b33"

def gaode_geocode(gps):
    url = f'https://restapi.amap.com/v3/geocode/regeo?output=xml&location={gps[0]},{gps[1]}&key={key}&radius=0&extensions=all'
    res = requests.get(url)
    text = res.content.decode()
    text = text.replace("</formatted_address>","<formatted_address>")
    formatted_address = text.split("<formatted_address>")[1]
    return formatted_address
