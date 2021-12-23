import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

pixels = neopixel.NeoPixel( board.D18, 12, auto_write=False )

pixels.brightness = 0.5   # make less blinding

# pixels[0] = fancy.CRGB(255, 255, 255).pack()
# pixels[3] = fancy.CRGB(255, 255, 255).pack()
# pixels[6] = fancy.CRGB(255, 255, 255).pack()
pixels[9] = fancy.CRGB(255, 255, 255).pack()

while True:
    pixels.show()
