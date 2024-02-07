
import math

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

LED_COUNT = 74

led_tab = {}

def classic(note):
    nb = note - 21
    temp = ((conversion(nb%12) + (nb//12)*7) / 52) * LED_COUNT - 0.21
    floor = math.floor(temp)
    ceil = math.ceil(temp)
    ef = round(temp - floor, 2)
    ec = round(ceil - temp, 2)

    return {floor:ef, ceil:ec}

def add_led(nb, v):
    led_tab[nb] = v

def rem_led(nb):
    led_tab.pop(nb)

STEP = 0.10

def refresh_strip():
    for i in led_tab:
        if(led_tab[i] > 0):
            print("ledColor("+str(i)+", "+str(led_tab[i])+")")
            led_tab[i] -= STEP
            if(led_tab[i] < 0):
                led_tab[i] = 0

add_led(23, 0.5)
add_led (22, 0.75)

rem_led(23)

for i in range(10):
    refresh_strip()


