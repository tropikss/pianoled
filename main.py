import mido
import time
from rpi_ws281x import PixelStrip, Color

# Configuration des LEDs
LED_COUNT = 75         # Nombre total de LEDs dans la bande
LED_PIN = 18           # GPIO utilisé pour contrôler les LEDs
LED_FREQ_HZ = 800000   # Fréquence des LEDs (ne pas modifier)
LED_DMA = 10           # Canal DMA utilisé pour transmettre les données aux LEDs (ne pas modifier)
LED_BRIGHTNESS = 50   # Luminosité des LEDs (0 à 255)
LED_INVERT = False     # Inverser le signal de données (True ou False)
LED_CHANNEL = 0        # Numéro du canal matériel utilisé pour les LEDs (0 ou 1)

# Initialisation de la bande de LEDs
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

red = Color(255, 0, 0)

black = Color(0, 0, 0)

def ledOn(nb):
    strip.setPixelColor(nb, red)
    pixels.show()

def ledOff(nb):
    strip.setPixelColor(nb, black)
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
            v = int(((msg.note-22)/88)*75)
            ledOn(v)
            print(f"Notes appuyées : {notes_appuyees}")
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            v = int(((msg.note-22)/88)*75)
            ledOff(v)
            notes_appuyees.discard(msg.note)
            print(f"Notes appuyées : {notes_appuyees}")
except KeyboardInterrupt:
    print("\nLecture arrêtée.")
finally:
    midi_port.close()