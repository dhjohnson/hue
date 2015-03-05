#!/usr/bin/python
#Turns on the hue lights in a random order and sets them to red
import time
import random
from phue import Bridge
b  = Bridge('192.168.1.140')
#b.connect()
lights = b.get_light_objects('id')
attempt = 0
wait = 0.1
while attempt == 0:
	time.sleep(wait)
	for light in lights:
		lights[light].on = False
	time.sleep(wait)
	for light in random.sample(lights, len(lights)):
		command = {'transitiontime' : int(wait*10), 'on' : True, 'hue' : 0, 'sat' : 254, 'bri' : 254}
		b.set_light(light, command)
		time.sleep(wait)
	wait = wait + 0.1
