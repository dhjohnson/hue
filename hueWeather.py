#!/usr/bin/python
#Sets the color of the hue lamps according to the weather
import urllib2
import json
import pickle
import syslog
from phue import Bridge
from datetime import time, datetime
# Connect to the hue bridge
b  = Bridge('192.168.1.140')
isFreezing = pickle.load(open("/home/david/hue/freezing.p", "rb"))
currentcolor = pickle.load(open("/home/david/hue/color.p", "rb"))
sunrise = pickle.load(open("/home/david/hue/sunrise.p", "rb"))
sunset = pickle.load(open("/home/david/hue/sunset.p", "rb"))
# Determine the lights we should use, based on the time of day
now = datetime.now()
kidswakeup = now.replace(hour=7, minute=0, second=0, microsecond=0)
kidsbedtime = now.replace(hour=18, minute=40, second=0, microsecond=0)
if kidswakeup < now < kidsbedtime:
    lights = b.get_light_objects('id')
    lights = lights.keys()
else:
    lights = b.get_group(1,'lights') #1 is the LivingRoom group
    lights = [int(x) for x in lights]
# Fetch the weather data from the API
f = urllib2.urlopen('http://api.wunderground.com/api/')
json_string = f.read()
parsed_json = json.loads(json_string)
weather = parsed_json['current_observation']['icon']
temp_f = parsed_json['current_observation']['temp_f']
f.close()
# print "It's", weather, "and", temp_f, "degrees at", now
syslog.syslog(syslog.LOG_ERR, "It's " + weather + " and " + str(temp_f) + " degrees")
# Set the lights to red if temp_f rises above 32
if temp_f > 32 and isFreezing == 1:
    command = {'hue' : 0, 'sat' : 254, 'bri' : 254}
    b.set_light(lights, command)
    isFreezing = 0
# Set the lights to blue if temp_f drops below 32
if temp_f <= 32 and isFreezing == 0:
    command = {'hue' : 47675, 'sat' : 254, 'bri' : 254}
    b.set_light(lights, command)
    isFreezing = 1
pickle.dump(isFreezing, open("/home/david/hue/freezing.p", "wb"))
# Turn our weather into a color
if weather in ('cloudy', 'mostlycloudy', 'partlycloudy'):
    color = 'dim gray'
elif weather == 'rain':
    color = 'green'
elif weather in ('clear', 'mostlysunny', 'partlysunny', 'sunny'):
    color = 'cornflower blue'
elif weather in ('snow', 'flurries'):
    color = 'white'
elif weather in ('fog', 'hazy'):
    color = 'yellow'
elif weather == 'sleet':
    color = 'pink'
elif weather == 'tstorms':
    color = 'purple'
# If we have a new color, change the lights
if color != currentcolor:
    if color == 'dim gray':
        command = {'hue' : 39796, 'sat' : 111, 'bri' : 90}
    elif color == 'green'  :
        command = {'hue' : 24000, 'sat' : 254, 'bri' : 254}
    elif color == 'cornflower blue':
        command = {'hue' : 48345, 'sat' : 190, 'bri' : 254}
    elif color == 'white':
        command = {'hue' : 39796, 'sat' : 111, 'bri' : 254}
    elif color == 'yellow':
        command = {'hue' : 15500, 'sat' : 254, 'bri' : 254}
    elif color == 'pink':
        command = {'hue' : 56695, 'sat' : 254, 'bri' : 254}
    elif color == 'purple':
        command = {'hue' : 51332, 'sat' : 254, 'bri' : 254}
    b.set_light(lights, command)
    pickle.dump(color, open("/home/david/hue/color.p", "wb"))
if datetime.now().time() < sunrise or datetime.now().time() > sunset:
    command = {'bri': 0}
    b.set_light(lights, command)
