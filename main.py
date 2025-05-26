import keyboard
import time

def read_commands_from_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            # Jede Zeile eine Taste oder Kombination, leere Zeilen ignorieren
            commands = [line.strip() for line in file if line.strip()]
        return commands
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {filepath}")
        return []

def execute_commands(commands,delay=0.1):
    print("Starte Tastensimulation in 3 Sekunden...")
    time.sleep(3)
    for command in commands:
        try:
            print(f"Sende: {command}")
            keyboard.send(command)
            time.sleep(delay)  # Pause zwischen Eingaben
        except Exception as e:
            print(f"Fehler bei '{command}': {e}")

if __name__ == "__main__":
    dateiname = "tasteneingaben.txt"  # Pfad zur Datei
    befehle = read_commands_from_file(dateiname)
    if befehle:
        execute_commands(befehle)
    else:
        print("Keine gültigen Befehle gefunden.")
