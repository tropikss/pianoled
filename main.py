import mido
import time
from rpi_ws281x import PixelStrip, Color
import math

# Configuration des LEDs
LED_COUNT = 75         # Nombre total de LEDs dans la bande
LED_PIN = 18           # GPIO utilisé pour contrôler les LEDs
LED_FREQ_HZ = 800000   # Fréquence des LEDs (ne pas modifier)
LED_DMA = 10           # Canal DMA utilisé pour transmettre les données aux LEDs (ne pas modifier)
LED_BRIGHTNESS = 10   # Luminosité des LEDs (0 à 255)
LED_INVERT = False     # Inverser le signal de données (True ou False)
LED_CHANNEL = 0        # Numéro du canal matériel utilisé pour les LEDs (0 ou 1)

# Initialisation de la bande de LEDs
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

red = Color(255, 0, 0)

black = Color(0, 0, 0)

def getColor(intensite):

    # Convertir l'intensité en une valeur entre 0 et 255
    valeur = int(intensite * 2.55)
    
    # Déterminer la couleur en fonction de l'intensité
    if valeur <= 127:
        # Bleu à vert
        rouge = 0
        vert = valeur * 2
        bleu = 255 - valeur * 2
    else:
        # Vert à rouge
        rouge = (valeur - 128) * 2
        vert = 255 - (valeur - 128) * 2
        bleu = 0
    
    # Retourner la couleur
    return Color(rouge, vert, bleu)

def ledIntensite(nb):
    v = getColor(nb)
    strip.setPixelColor(nb, v)
    strip.show()

def ledOn(nb):
    strip.setPixelColor(nb, red)
    strip.show()

def ledOff(nb):
    strip.setPixelColor(nb, black)
    strip.show()

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
            v = math.ceil(((msg.note-22)/88)*75)
            ledIntensite(v)
            print(f"Notes appuyees : {notes_appuyees}")
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            v = math.ceil(((msg.note-22)/88)*75)
            ledOff(v)
            notes_appuyees.discard(msg.note)
            print(f"Notes appuyées : {notes_appuyees}")
except KeyboardInterrupt:
    print("\nLecture arrêtée.")
finally:
    midi_port.close()