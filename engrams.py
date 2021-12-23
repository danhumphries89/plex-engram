import time
import random
import board 
import neopixel

# The fading functionlity might only be neccesary when swapping between songs
# It looks like the Engrams are just lit up to begin with, need to investigate further

# Engram Colours
engrams_white  = ( 123, 123, 136 )
engrams_green  = ( 74, 120, 59 )
engrams_blue   = ( 67, 94, 198 )
engrams_purple = ( 102, 40, 180 )
engrams_yellow = ( 162, 119, 47 )

engrams = [ engrams_white, engrams_green, engrams_blue, engrams_purple, engrams_yellow ]

# NeoPixel & Fade Settings
start_brightness = 0.2
max_brightness = 0.65
fade_duration = 20
max_intervals = 5
interval_duration = 0.25
interval_counter = 0

# Prepare the NeoPixel
pixels = neopixel.NeoPixel( board.D18, 12, brightness = start_brightness )

# Randomly Select & Fill the Colour
pixels.fill( random.choice( engrams ) )


while True:

	while (pixels.brightness < max_brightness):
		pixels.brightness = pixels.brightness + ( max_brightness / fade_duration )
		time.sleep( max_brightness / fade_duration  )

	# Stop the Loop if we're at the max_intervals limit
	if interval_counter == max_intervals:
		pixels.brightness = max_brightness
		break

	# Pause for alloted time before reversing
	time.sleep( interval_duration + 1 )

	while (pixels.brightness > start_brightness):
		pixels.brightness = pixels.brightness - ( max_brightness / fade_duration )
		time.sleep( max_brightness / fade_duration )

	# Pause for variable time before we continue
	time.sleep( interval_duration )

	# Increment the Counter to find the stop position
	interval_counter = interval_counter + 1
