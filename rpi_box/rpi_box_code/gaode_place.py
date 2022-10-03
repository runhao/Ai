import json
import requests

key = "a4bd20595b6e9ea56857fa9d7d114b33"

def gaode_place(locate):
    url = "http://httpbin.org/ip"
    res = requests.get(url)
    ip = json.loads(res.text)["origin"]    #获取ip,关键字搜索
    url = f'https://restapi.amap.com/v3/ip?ip={ip}&output=xml&key={key}'
    res = requests.get(url)
    text = res.content.decode()
    city = text.replace("</city>","<city>").split("<city>")[1]
    url = f'https://restapi.amap.com/v3/place/text?keywords={locate}&city={city}&output=xml&offset=1&page=1&key={key}&extensions=base'
    res = requests.get(url)
    text = res.content.decode()
    origin = text.replace("</location>","<location>").split("<location>")[1]
    return origin
