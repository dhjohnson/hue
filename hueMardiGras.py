#!/usr/bin/python
#http://serennu.com/colour/hsltorgb.php
#Sets the Hue light strips randomly to purple, yellow or green
import time
import random
from phue import Bridge
b  = Bridge('192.168.1.140')
b.connect()
time.sleep(5)
command = {'hue' : 51332, 'sat' : 254, 'bri' : 254}
b.set_light([1,2,3,4], command)
attempt = 0
wait = 0.1
while attempt == 0:
	for l in range(1,5):
		r = random.randint(1, 6)
		if r <= 3:
			# set to purple
			b.set_light(l, 'hue', 51332, transitiontime=int(wait*10))
		elif r<= 5:
			# set to yellow
			b.set_light(l, 'hue', 15500, transitiontime=int(wait*10))
		else:
			# set to green
			b.set_light(l, 'hue', 24000, transitiontime=int(wait*10))
		time.sleep(wait)
	wait = wait + 0.1
