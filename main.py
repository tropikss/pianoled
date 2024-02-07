import mido
import time
from rpi_ws281x import PixelStrip, Color
import math

# Configuration des LEDs
LED_COUNT = 74         # Nombre total de LEDs dans la bande
LED_PIN = 18           # GPIO utilisé pour contrôler les LEDs
LED_FREQ_HZ = 800000   # Fréquence des LEDs (ne pas modifier)
LED_DMA = 10           # Canal DMA utilisé pour transmettre les données aux LEDs (ne pas modifier)
LED_BRIGHTNESS = 50   # Luminosité des LEDs (0 à 255)
LED_INVERT = False     # Inverser le signal de données (True ou False)
LED_CHANNEL = 0        # Numéro du canal matériel utilisé pour les LEDs (0 ou 1)

# Initialisation de la bande de LEDs
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Parametre de controle 
STEP = 0.03

# Couleur prédéfinies
red = Color(255, 0, 0)
black = Color(0, 0, 0)

def get_blue_gradient(percentage):
    """
    Renvoie un triplet d'entiers représentant une couleur bleue allant d'un bleu ciel à un bleu profond.
    Le pourcentage doit être compris entre 0 et 100.
    """
    # Définition des couleurs de référence
    sky_blue = (135, 206, 250)  # Bleu ciel
    deep_blue = (0, 0, 139)      # Bleu profond
    
    # Calcul de la couleur intermédiaire en fonction du pourcentage
    r = sky_blue[0] + int((deep_blue[0] - sky_blue[0]) * percentage / 100)
    g = sky_blue[1] + int((deep_blue[1] - sky_blue[1]) * percentage / 100)
    b = sky_blue[2] + int((deep_blue[2] - sky_blue[2]) * percentage / 100)
    
    return (r, g, b)

def get_orange_gradient(percentage):
    """
    Renvoie un triplet d'entiers représentant une couleur orange allant d'un orange clair à un orange profond.
    Le pourcentage doit être compris entre 0 et 100.
    """
    # Définition des couleurs de référence
    light_orange = (255, 165, 0)  # Orange clair
    deep_orange = (255, 69, 0)    # Orange profond
    
    # Calcul de la couleur intermédiaire en fonction du pourcentage
    r = light_orange[0] + int((deep_orange[0] - light_orange[0]) * percentage / 100)
    g = light_orange[1] + int((deep_orange[1] - light_orange[1]) * percentage / 100)
    b = light_orange[2] + int((deep_orange[2] - light_orange[2]) * percentage / 100)
    
    return (r, g, b)

def conversion(argument):
    switcher = {
        0: lambda: 1,
        1: lambda: 1.5,
        2: lambda: 2,
        3: lambda: 3,
        4: lambda: 3.5,
        5: lambda: 4,
        6: lambda: 4.5,
        7: lambda: 5,
        8: lambda: 6,
        9: lambda: 6.5,
        10: lambda: 7,
        11: lambda: 7.5,
    }
    return switcher.get(argument, lambda: "Valeur invalide")()

led_tab = {}

def add_led(nb, v):
    led_tab[nb] = v

def rem_led(nb):
    if nb in led_tab:
        del led_tab[nb]

def refresh_strip():
    to_remove = []
    for i in led_tab:
        if(led_tab[i] > 0):
            couleur = getColor((i/LED_COUNT)*100)
            ledColor(i, couleur, led_tab[i])
            led_tab[i] = round(led_tab[i] - STEP, 2)
        else:
            to_remove.append(i)
    for i in to_remove:
        ledOff(i)
        if i in led_tab:
            del led_tab[i]

def getColor(percentage):
    """
    Renvoie un triplet d'entiers représentant une couleur en fonction du pourcentage donné.
    Le pourcentage doit être compris entre 0 et 100.
    """
    # Définition des couleurs de référence
    rouge = (255, 0, 0)
    jaune = (255, 255, 0)
    vert = (0, 255, 0)
    cyan = (0, 255, 255)
    bleu = (0, 0, 255)
    magenta = (255, 0, 255)
    
    # Séparation du pourcentage en intervalles correspondant à différentes transitions de couleur
    if percentage < 20:
        # Transition de rouge à jaune
        r1 = rouge[0] + int((jaune[0] - rouge[0]) * percentage / 20)
        g1 = rouge[1] + int((jaune[1] - rouge[1]) * percentage / 20)
        b1 = rouge[2] + int((jaune[2] - rouge[2]) * percentage / 20)
        return (r1, g1, b1)
    elif percentage < 40:
        # Transition de jaune à vert
        r2 = jaune[0] + int((vert[0] - jaune[0]) * (percentage - 20) / 20)
        g2 = jaune[1] + int((vert[1] - jaune[1]) * (percentage - 20) / 20)
        b2 = jaune[2] + int((vert[2] - jaune[2]) * (percentage - 20) / 20)
        return (r2, g2, b2)
    elif percentage < 60:
        # Transition de vert à cyan
        r3 = vert[0] + int((cyan[0] - vert[0]) * (percentage - 40) / 20)
        g3 = vert[1] + int((cyan[1] - vert[1]) * (percentage - 40) / 20)
        b3 = vert[2] + int((cyan[2] - vert[2]) * (percentage - 40) / 20)
        return (r3, g3, b3)
    elif percentage < 80:
        # Transition de cyan à bleu
        r4 = cyan[0] + int((bleu[0] - cyan[0]) * (percentage - 60) / 20)
        g4 = cyan[1] + int((bleu[1] - cyan[1]) * (percentage - 60) / 20)
        b4 = cyan[2] + int((bleu[2] - cyan[2]) * (percentage - 60) / 20)
        return (r4, g4, b4)
    else:
        # Transition de bleu à magenta
        r5 = bleu[0] + int((magenta[0] - bleu[0]) * (percentage - 80) / 20)
        g5 = bleu[1] + int((magenta[1] - bleu[1]) * (percentage - 80) / 20)
        b5 = bleu[2] + int((magenta[2] - bleu[2]) * (percentage - 80) / 20)
        return (r5, g5, b5)
    
    # Retourner la couleur
    return (rouge, vert, bleu)

def ledColor(numero_led, couleur, intensite):
    strip.setPixelColor(numero_led, Color(int(couleur[0] * intensite), int(couleur[1] * intensite), int(couleur[2] * intensite)))
    strip.show()

def ledOff(nb):
    strip.setPixelColor(nb, black)
    strip.show()

# Affiche tous les ports MIDI disponibles
port = mido.get_input_names()
print(mido.get_input_names())

notes_appuyees = {}


# Choisis le port MIDI approprié
port_name = port[1]
midi_port = mido.open_input(port_name)

oldmsg = mido.Message('note_on', note=0, velocity=0, time=0)

i = 0

try:
    for msg in midi_port:

        if(msg.type != 'clock' and msg.type != 'control_change'):
            print(msg.type)
            nb = msg.note - 21
            temp = ((conversion(nb%12) + (nb//12)*7) / 52) * LED_COUNT - 0.21
            ceil = math.ceil(temp)
            ec = round(ceil - temp, 2)

        if msg.type == 'note_on' and msg.velocity > 0:
            notes_appuyees[msg.note] = ceil-1
            i += 1

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in notes_appuyees:
                del notes_appuyees[msg.note]
        
        for u in notes_appuyees:
            add_led(notes_appuyees[u], 0.5)
            i += 1

        print(led_tab)
        refresh_strip()

        if i > 100:
            i = 0

except KeyboardInterrupt:
    print("\nLecture arrêtée.")
finally:
    midi_port.close()