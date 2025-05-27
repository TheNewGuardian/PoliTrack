import keyboard

def record_repeated_keys_to_txt(filename="tasteneingaben.txt"):
    print("Aufzeichnung startet. Drücke ESC zum Beenden.")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            while True:
                event = keyboard.read_event()
                
                # Nur auf Tastendruck reagieren
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == "esc":
                        print("Aufzeichnung beendet.")
                        break
                    file.write(event.name + "\n")
                    file.flush()  # Sofort in Datei schreiben

    except Exception as e:
        print(f"Fehler beim Schreiben der Datei: {e}")




record_repeated_keys_to_txt()