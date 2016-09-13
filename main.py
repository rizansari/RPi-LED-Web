import RPi.GPIO
import os, time
from bottle import route, run, template, static_file, get
from random import randint

host = "0.0.0.0"
port = 8081

led_red_pin = 18
led_yellow_pin = 23

global led_red_state
led_red_state = False
global led_yellow_state
led_yellow_state = False
	
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(led_red_pin, RPi.GPIO.OUT)
RPi.GPIO.setup(led_yellow_pin, RPi.GPIO.OUT)

RPi.GPIO.output(led_red_pin, led_red_state)
RPi.GPIO.output(led_yellow_pin, led_yellow_state)


@route('/')
def index():
	return template('main.html')
	
# Static Routes
@get('/<filename:re:.*\.(js|css|jpg|png|gif|ico|eot|ttf|woff|svg)>')
def javascripts(filename):
    return static_file(filename, root='static')

@route('/led/<led>/<state>')
def led(led, state):
	global led_red_state
	global led_yellow_state
	
	if led == "1":
		if state == "true":
			RPi.GPIO.output(led_red_pin, True)
			led_red_state = True
		else:
			RPi.GPIO.output(led_red_pin, False)
			led_red_state = False
	
	if led == "2":
		if state == "true":
			RPi.GPIO.output(led_yellow_pin, True)
			led_yellow_state = True
		else:
			RPi.GPIO.output(led_yellow_pin, False)
			led_yellow_state = False

	return 'led' + led + ' ' + state
	
@route('/led/<led>')
def led(led):
	global led_red_state
	global led_yellow_state
	
	if led == "1":
		return str(led_red_state)
	
	if led == "2":
		return str(led_yellow_state)

try:
	run(host=host, port=port)
except KeyboardInterrupt:
	#cleanup
	shutdown()
except:
	shutdown()
