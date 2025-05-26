import keyboard

def record_keys_to_txt(filename="tasteneingaben.txt"):
    print("Die Aufzeichnung beginnt. Drücke ESC zum Beenden.")
    events = keyboard.record(until='esc')
    
    # 'esc' nicht speichern
    filtered_keys = [event.name for event in events if event.event_type == 'down' and event.name != 'esc']

    try:
        with open(filename, "w", encoding="utf-8") as file:
            for key in filtered_keys:
                file.write(key + "\n")
        print(f"Tasten wurden erfolgreich in '{filename}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Schreiben der Datei: {e}")

record_keys_to_txt()