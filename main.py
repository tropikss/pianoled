import mido
import neopixel

import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 75     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Allumer 3 LEDs en rouge
for i in range(3):
    pixels[i] = (255, 0, 0)  # Rouge

# Mise à jour des LEDs pour afficher les changements
pixels.show()

# Affiche tous les ports MIDI disponibles
port = mido.get_input_names()
print(mido.get_input_names())

notes_appuyees = set()

# Choisis le port MIDI approprié
port_name = port[1]
midi_port = mido.open_input(port_name)

oldmsg = mido.Message('note_on', note=0, velocity=0, time=0)
try:
    for msg in midi_port:
        if msg.type == 'note_on' and msg.velocity > 0:
            notes_appuyees.add(msg.note)
            print(f"Notes appuyées : {notes_appuyees}")
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            notes_appuyees.discard(msg.note)
            print(f"Notes appuyées : {notes_appuyees}")
except KeyboardInterrupt:
    print("\nLecture arrêtée.")
finally:
    midi_port.close()