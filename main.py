import mido
import board
import neopixel

# Configuration des LEDs
NUM_LEDS = 75  # Nombre total de LEDs dans la bande
PIN_LED = board.D18  # Port GPIO auquel les LEDs sont connectées
BRIGHTNESS = 0.5  # Luminosité des LEDs (0 à 1)

# Initialisation de la bande de LEDs
pixels = neopixel.NeoPixel(PIN_LED, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

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