import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

pixels = neopixel.NeoPixel( board.D18, 12, brightness = 0.25, auto_write = False)

palette = [fancy.CRGB(255, 255, 255),  # White
           fancy.CRGB(255, 255, 0),    # Yellow
           fancy.CRGB(255, 0, 0),      # Red
           fancy.CRGB(0,0,0)]          # Black

offset = 0  # Position offset into palette to make it "spin"

while True:
    for i in range(12):
        color = fancy.palette_lookup(palette, offset + i / 9)
        pixels[i] = color.pack()
    pixels.show()

    offset += 0.001  # Bigger number = faster spin