#!/usr/bin/python
#http://serennu.com/colour/hsltorgb.php
import time
import json
from phue import Bridge
b  = Bridge('192.168.1.140')
b.connect()
b.set_light([1,2,3], 'on', False)
time.sleep(5)
# Sets the Middle light (2) to white, then the outside lights
command = {'transitiontime' : 0, 'on' : True, 'hue' : 39796, 'bri' : 254, 'sat' : 111}
b.set_light(2, command)
time.sleep(0)
b.set_light([1,3], command)
time.sleep(0)
attempt = 0
wait = float(0.1)
while attempt == 0:
	# Sets the Middle light (2) to pink, then the outside lights
	command = {'transitiontime' : int(wait*10), 'hue' : 56695, 'sat' : 254}
	b.set_light(2, command)
	time.sleep(wait)
	command = {'transitiontime' : int(wait*30), 'hue' : 56695, 'sat' : 254}
	b.set_light([1,3], command)
	time.sleep(wait*3)
	# Sets the Middle light (2) to red (3286)
	b.set_light(2, 'hue', 3286, transitiontime=int(wait*10))
	time.sleep(wait)
	# Sets the Outside lights to red (3286)
	b.set_light([1,3], 'hue', 3286, transitiontime=int(wait*30))
	time.sleep(wait*3)
	# Sets the Middle light (2) to purple (51332)
	b.set_light(2, 'hue', 51332, transitiontime=int(wait*10))
	time.sleep(wait)
	# Sets the Outside lights to purple (51332)
	b.set_light([1,3], 'hue', 51332, transitiontime=int(wait*30))
	time.sleep(wait*3)
	# Sets the Middle light (2) to white
	command = {'transitiontime' : int(wait*10), 'hue' : 39796, 'sat' : 111}
	b.set_light(2, command)
	time.sleep(wait)
	# Sets the Outside lights to white
	command = {'transitiontime' : int(wait*20), 'hue' : 39796, 'sat' : 111}	
	b.set_light([1,3], command)
	time.sleep(wait*3)
	wait = wait + 0.1
