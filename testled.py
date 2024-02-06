import time
from rpi_ws281x import PixelStrip, Color

# Configuration des LEDs
LED_COUNT = 75         # Nombre total de LEDs dans la bande
LED_PIN = 18           # GPIO utilisé pour contrôler les LEDs
LED_FREQ_HZ = 800000   # Fréquence des LEDs (ne pas modifier)
LED_DMA = 10           # Canal DMA utilisé pour transmettre les données aux LEDs (ne pas modifier)
LED_BRIGHTNESS = 255   # Luminosité des LEDs (0 à 255)
LED_INVERT = False     # Inverser le signal de données (True ou False)
LED_CHANNEL = 0        # Numéro du canal matériel utilisé pour les LEDs (0 ou 1)

# Initialisation de la bande de LEDs
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def allumer_trois_premieres_leds(couleur):
    """
    Allume les trois premières LEDs de la bande avec la couleur spécifiée.

    Args:
        couleur (tuple): Tuple contenant les valeurs RGB de la couleur des LEDs (ex: (255, 0, 0) pour rouge).
    """
    # Allumer les trois premières LEDs avec la couleur spécifiée
    for i in range(3):
        strip.setPixelColor(i, Color(*couleur))
    strip.show()

# Exemple d'utilisation : Allumer les trois premières LEDs en rouge
allumer_trois_premieres_leds((255, 0, 0))  # Rouge