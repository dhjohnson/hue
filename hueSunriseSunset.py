#!/usr/bin/python
#Schedules the color of the hue lamps according to the sun and the kids bedtime
import urllib2
import json
import pickle
from datetime import datetime, date, time, timedelta
from phue import Bridge
# Connect to the hue bridge
b  = Bridge('192.168.1.140')
sleepIn = 0 # Set this to 1 delay the kids wakeup on a weekday
# Get and parse the sunrise and sunset data from the API
f = urllib2.urlopen('http://api.wunderground.com/api/')
json_string = f.read()
parsed_json = json.loads(json_string)
sRhour = parsed_json['sun_phase']['sunrise']['hour']
sRminute = parsed_json['sun_phase']['sunrise']['minute']
sShour = parsed_json['sun_phase']['sunset']['hour']
sSminute = parsed_json['sun_phase']['sunset']['minute']
f.close
# Set up the time stings when the scheduled commands will take place
today = date.today()
UTCoffset = datetime.utcnow() - datetime.now()
sRtime = time(int(sRhour), int(sRminute))
sStime = time(int(sShour), int(sSminute))
sSlocalTS = datetime.combine(today, sStime)
sSUTC = sSlocalTS + UTCoffset
# Start the sunset program fifteen minutes before the sun actually sets
sSUTCstart = sSUTC - timedelta(minutes=15)
sSUTCstring = sSUTCstart.strftime ("%Y-%m-%dT%H:%M:%S")
# Set the group 1 (living room) lights to yellow
data = {'hue': 15500, 'sat': 254, 'bri': 254}
b.create_group_schedule('Living room sunset prep', sSUTCstring, 1, data, 'turn yellow')
# Then, a second later, change them to dim red over the next 30 minutes
sSUTCstart2 = sSUTCstart + timedelta(seconds=1)
sSUTCstring2 = sSUTCstart2.strftime ("%Y-%m-%dT%H:%M:%S")
data = {'hue': 0, 'bri': 0, 'transitiontime': 18000}
b.create_group_schedule('Living room sunset', sSUTCstring2, 1, data, 'dim to red')
# Set the bulb to turn on at 1845
almostbedtime = time (18, 45)
ablocalTS = datetime.combine(today, almostbedtime)
abUTC = ablocalTS + UTCoffset
abUTCstring = abUTC.strftime ("%Y-%m-%dT%H:%M:%S")
data = {'hue': 14922, 'sat': 144,'bri': 254}
b.create_schedule('Kids almost bedtime', abUTCstring, 4, data, 'turn on white')
# Set the bulb to yellow just before 1925
yellowtime = time (19,24,59)
ylocalTS = datetime.combine(today, yellowtime)
yUTC = ylocalTS + UTCoffset
yUTCstring = yUTC.strftime ("%Y-%m-%dT%H:%M:%S")
data = {'hue': 15500, 'sat': 254, 'bri': 254}
b.create_schedule('Kids sunset prep', yUTCstring, 4, data, 'turn yellow')
# Then, a second later, change them to dim red over the next 5 minutes
yUTC2 = yUTC + timedelta(seconds=1)
yUTCstring2 = yUTC2.strftime ("%Y-%m-%dT%H:%M:%S")
data = {'hue': 0, 'bri': 0, 'transitiontime': 3000}
b.create_schedule('Kids sunset', yUTCstring2, 4, data, 'dim to red')
# Finally, turn off the light
offtime = time (19,30,00)
offTS = datetime.combine(today, offtime)
offUTC = offTS + UTCoffset
offUTCstring = offUTC.strftime ("%Y-%m-%dT%H:%M:%S")
data = {'on': False}
b.create_schedule('Kids off', offUTCstring, 4, data, 'turn off')
# Set the kid's light to green on weekend mornings
if today.weekday() > 5 or sleepIn == 1:
    weekendwakeup = time (7,00)
    weekendwakeupTS = datetime.combine(today, weekendwakeup)
    weUTC = weekendwakeupTS + UTCoffset
    weUTCstring = weUTC.strftime ("%Y-%m-%dT%H:%M:%S")
    data = {'on': True, 'hue': 24000, 'sat': 254, 'bri': 0}
    b.create_schedule('Kids weekend on', weUTCstring, 4, data, 'weekend turn on')
else:
    weekdaywakeup = time (6,30)
    weekdaywakeupTS = datetime.combine(today, weekdaywakeup)
    wdUTC = weekdaywakeupTS + UTCoffset
    wdUTCstring = wdUTC.strftime ("%Y-%m-%dT%H:%M:%S")
    data = {'on': True, 'hue': 15500, 'sat': 254, 'bri': 254, 'transitiontime': 600}
    b.create_schedule('Kids weekday sunrise', wdUTCstring, 4, data, 'weekday wakeup')
    getreadytime = time (6, 31)
    getreadyTS = datetime.combine(today, getreadytime)
    grUTC = getreadyTS + UTCoffset
    grUTCstring = grUTC.strftime ("%Y-%m-%dT%H:%M:%S")
    data = {'hue': 14922, 'sat': 144,'bri': 254}
    b.create_schedule('Kids weekday get ready', grUTCstring, 4, data, 'turn on white')
pickle.dump(sRtime, open("/home/david/hue/sunrise.p", "wb"))
pickle.dump(sStime, open("/home/david/hue/sunset.p", "wb"))
