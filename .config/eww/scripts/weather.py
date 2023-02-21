#!/usr/bin/env python

import os
import sys
import json
import time
import requests
import datetime

lat, lon=30.5349, 47.7888

icons = {
    'DEFAULT': '\uf185', '01d': '\uf185', '01n': '\uf186', '02d': '\uf6c4',
    '02n': '\uf6c3', '03d': '\uf0c2', '03n': '\uf0c2', '04d': '\uf0c2',
    '04n': '\uf0c2', '09d': '\uf740', '09n': '\uf740', '10d': '\uf743',
    '10n': '\uf73c', '11d': '\uf0e7', '11n': '\uf0e7', '12d': '\uf2dc',
    '12n': '\uf2dc', '50d': '\uf72e', '50n': '\uf72e'}

path = os.path.expanduser('~/Scripts/LemonBar/OPENWEATHER_APIKEY') if len(sys.argv) < 2 else sys.argv[1]
with open(path, 'r') as f:
    apikey = f.read().strip()

obj = {'last_updated': 'Loading..'}
try:
    req_link = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={apikey}&units=metric"
    response = requests.get(req_link)
    response = response.json()
    icon = icons.get(response['current']['weather'][0]['icon'], icons['DEFAULT'])
    last_update = datetime.datetime.now().strftime('last updated on: %H:%M %a')
    obj = {"icon": icon, "temp": f'{response["current"]["temp"]:0.0f}',
            'last_updated': last_update}
    print(json.dumps(obj))
except Exception:
    print(json.dumps({'icon': '\ue137', 'temp': '', 'last_updated': obj["last_updated"]}))
    sys.exit()
