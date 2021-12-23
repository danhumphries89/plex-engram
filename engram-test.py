#! /usr/bin/env python

from os import confstr
import time
import random
import argparse
import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import AMBER

# Parser
# Prepare our CMD parameter parser to grab what Engram Type should be decoded
# @URL: https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser( description='Decode the Engram supplied based on the music playing in our Plex Library' )
parser.add_argument( 'type', default="encoded", help="The Engram type we want to decode")
parser.add_argument( '--stop', action="store_true", help="Stop the Engram decoding")

# Prepare the Arguments based on what the user has entered
args = parser.parse_args()

# The fading functionlity might only be neccesary when swapping between songs
# It looks like the Engrams are just lit up to begin with, need to investigate further

# Engram Colours
# fancy.gamma_adjust()
# engram_gamma_adjustment = (0.25, 0.3, 0.15)
engram_dictionary = {
	'encoded':		fancy.gamma_adjust(fancy.CRGB( 182, 174, 165 )),
	'encrypted':	fancy.gamma_adjust(fancy.CRGB( 43, 94, 49 )),
	'decoherent':	fancy.gamma_adjust(fancy.CRGB( 88, 117, 159 )),
	'legendary': 	fancy.gamma_adjust(fancy.CRGB( 77, 49, 98 )),
	'exotic':		fancy.gamma_adjust(fancy.CRGB( 201, 176, 76 ))
}

# NeoPixel & Fade Settings
start_brightness = 0.2
max_brightness = 0.5
fade_duration = 20
max_intervals = 5

# Prepare the NeoPixel
pixels = neopixel.NeoPixel( board.D18, 12, brightness = max_brightness, auto_write = False)

def stop_pixels() :
	pixels.deinit()
	exit( 0 )

def update_pixels() :
	decoded_engram_color = engram_dictionary.get( args.type ).pack()
	pulse_cycle_limit = 5

	pulse = Pulse(
		pixels,
		speed = 0.1,
		color = decoded_engram_color,
		period = 2
	)

	# Introduce a Fake Pause to wait for skipping
	time.sleep( 10 )

	while pulse.cycle_count < pulse_cycle_limit :
		pulse.animate()

		if pulse.cycle_count == pulse_cycle_limit :
			pixels.fill( decoded_engram_color )
			pixels.show()

			# Finish everything
			exit( 0 )

# Update Pixels (Default)
if args.type and not args.stop :
	update_pixels()
else :
	print( "Stopping Pixels" )
	stop_pixels()