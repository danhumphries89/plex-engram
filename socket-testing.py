
import time
import os
import board 
import neopixel
import socketio

# @URL: https://kaliko.gitlab.io/python-musicpd/
import musicpd

# @URL: https://learn.adafruit.com/fancyled-library-for-circuitpython/overview
import adafruit_fancyled.adafruit_fancyled as fancy

# @URL: https://learn.adafruit.com/circuitpython-led-animations/basic-animations
from adafruit_led_animation.animation.pulse import Pulse


# The fading functionlity might only be neccesary when swapping between songs
# It looks like the Engrams are just lit up to begin with, need to investigate further

# Prepare the Gamma adjustment levels for the LEDs
# @URL: https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors
engram_gamma_adjustment = (0.25, 0.3, 0.15)

# Setup the Engram Colours
engrams_common  = fancy.gamma_adjust(fancy.CRGB( 182, 174, 165 ), brightness=engram_gamma_adjustment)
engrams_uncommon  = fancy.gamma_adjust(fancy.CRGB( 43, 94, 49 ), brightness=engram_gamma_adjustment)
engrams_rare   = fancy.gamma_adjust(fancy.CRGB( 88, 117, 159 ), brightness=engram_gamma_adjustment)
engrams_legendary = fancy.gamma_adjust(fancy.CRGB( 77, 49, 98 ), brightness=engram_gamma_adjustment)
engrams_exotic = fancy.gamma_adjust(fancy.CRGB( 201, 176, 76 ), brightness=engram_gamma_adjustment)

# NeoPixel + Fade Settings
start_brightness = 1.0
max_brightness = 0.65
fade_duration = 20
max_intervals = 5
interval_duration = 2

# Setup the Engram Dictionary
engrams = {
	"none" : engrams_common,
	"uncommon" : engrams_uncommon,
	"44.1" : engrams_rare,
	"88.2" : engrams_legendary,
	"96"   : engrams_legendary,
	"192"  : engrams_exotic
}

# Prepare the NeoPixel
pixels = neopixel.NeoPixel( board.D18, 12, brightness = start_brightness, auto_write=False )

# Prepare the SocketIO Client
sio = socketio.Client()

# Prepare our clear() script (might not be required soon)
clear = lambda: os.system('clear')

def checkEngrams( service, samplerate ):
	for engram in engrams.keys():
		if service == 'mpd':
			if samplerate and engram in samplerate:
				return engrams.get( engram )
		elif service == 'volspotconnect2':
			return engrams.get('uncommon')
		else:
			return engrams.get('none')

def changeEngramColour( engram_colour ) :

	pixels.brightness = start_brightness
	pixels.fill( engram_colour.pack() )
	pixels.show()

	# Not sure why the global variable isn't working
	interval_counter = 0

	# print('About to start the Pulse animation')
	# pulse_container = Pulse( pixels, speed=0.05, color=engram_colour.pack(), period=interval_duration )

	# while interval_counter < max_intervals:
		# pulse_container.animate()

	# 	while (pixels.brightness < max_brightness) :
	# 		pixels.brightness = pixels.brightness + ( max_brightness / fade_duration )
	# 		time.sleep( max_brightness / fade_duration  )

	# 		# Stop the Loop if we're at the max_intervals limit
	# 		if interval_counter == max_intervals:
	# 			print('finished with the fade animation')
	# 			pixels.brightness = max_brightness
	# 			break

	# 	# Pause for alloted time before reversing
	# 	time.sleep( interval_duration + 1 )

	# 	while (pixels.brightness > start_brightness):
	# 		pixels.brightness = pixels.brightness - ( max_brightness / fade_duration )
	# 		time.sleep( max_brightness / fade_duration )

	# 	# Pause for variable time before we continue
		# time.sleep( interval_duration + 1)

		# Increment the Counter to find the stop position
		# if pulse_container.cycle_count == 5 :
		# 	interval_counter += 1

def checkMPD() : 
	client = musicpd.MPDClient()
	client.connect()

	print( 'Currently Playing (MPD): ', client.currentsong() )

	client.disconnect()

@sio.event
def connect():
	print('connection established')

	clear()
	sio.emit('getState')


# Note: This doesn't always trigger when Spotify is active
# but there might be an SocketIO event that I can hook into
# to trigger another sio.emit('getState') like I do when the
# script runs to begin with

# Whole album play doesn't trigger this correctly. I'll need
# to hook into another event to trigger another getState

@sio.event
def pushState(data):
	# Clear the output in anticipation
	clear()

	print( data.get('status') )

	if data.get('status') == 'play' :
		# Basic Output of some information (not required in the end)
		print('Now Playing: ', data.get('title'))
		print('Source: ', data.get('stream'))
		print('Sample Rate: ', data.get('samplerate'))
		print('Service: ', data.get('service'))
		print('Engram Selection: ', checkEngrams( data.get('service'), data.get( 'samplerate' ) ))

		changeEngramColour( checkEngrams( data.get('service'), data.get( 'samplerate' ) ) )

	else :
		print('Nothing Playing')
		changeEngramColour( engrams.get( 'none' ) )

@sio.event
def connect_error( data ):
	print('connection failed: %s', data)

sio.connect('http://192.168.1.46:3000/')
sio.wait()
