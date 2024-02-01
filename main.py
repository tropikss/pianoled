import mido

# Affiche tous les ports MIDI disponibles
port = mido.get_input_names()
print(mido.get_input_names())

# Choisis le port MIDI approprié
port_name = port[1]
midi_port = mido.open_input(port_name)

print("Lecture des messages MIDI. Appuie sur Ctrl+C pour arrêter.")
oldmsg = None
try:
    for msg in midi_port:
        if(msg != oldmsg):
            print(msg)
            oldmsg = msg
except KeyboardInterrupt:
    print("\nLecture arrêtée.")
finally:
    midi_port.close()