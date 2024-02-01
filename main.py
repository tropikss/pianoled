import mido

# Affiche tous les ports MIDI disponibles
print(mido.get_input_names())

# Choisis le port MIDI approprié
port_name = "Nom de ton port MIDI"
midi_port = mido.open_input(port_name)

print("Lecture des messages MIDI. Appuie sur Ctrl+C pour arrêter.")

try:
    for msg in midi_port:
        print(msg)
except KeyboardInterrupt:
    print("\nLecture arrêtée.")
finally:
    midi_port.close()