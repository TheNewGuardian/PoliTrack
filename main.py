import gym
import numpy as np
import time
import cv2
import mss
from pynput.keyboard import Controller
import pygetwindow as gw
from stable_baselines3 import PPO
import pytesseract
import mss

# Tastatursteuerung
keyboard = Controller()

# Steuerungstasten
KEY_LEFT = "a"
KEY_RIGHT = "d"
KEY_ACCELERATE = "w"
KEY_BACKWARDS = "s"

# Aktiviere Trackmania-Fenster
def focus_trackmania():
    try:
        win = next(w for w in gw.getWindowsWithTitle("Trackmania") if w.visible)
        win.activate()
        time.sleep(1)
        print("Trackmania aktiviert.")
    except StopIteration:
        print("Trackmania-Fenster nicht gefunden.")

# Tastenbefehle senden
def press_key(key, duration=0.1):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

# Bildschirmaufnahme
def get_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))
        img = cv2.resize(screenshot, (84, 84))
        img = img[:, :, :3]  # RGB
        return img
    
def read_speed():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))
        img = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # HUD-Speed-Bereich zuschneiden (abhängig von Auflösung)
        # Beispiel: rechte untere Ecke (anpassen!)
        speed_crop = img[850:900, 1920:1080]  # für Full HD (1920x1080)

        # OCR durchführen
        text = pytesseract.image_to_string(speed_crop, config='--psm 7')
        
        # Nur Zahlen extrahieren
        try:
            speed = int(''.join(filter(str.isdigit, text)))
            return speed
        except:
            return 0

# RL-Umgebung definieren
class TrackmaniaEnv(gym.Env):
    def __init__(self):
        super(TrackmaniaEnv, self).__init__()

        # Aktionen: [0: nichts, 1: links, 2: rechts, 3: beschleunigen]
        self.action_space = gym.spaces.Discrete(4)

        # Beobachtung: 84x84 RGB-Bild
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)

    def reset(self):
        # Fokus auf Spiel
        focus_trackmania()
        time.sleep(1)
        return get_screen()

    def step(self, action):
        # Eingabe senden
        if action == 1:
            press_key(KEY_LEFT, 0.2)
        elif action == 2:
            press_key(KEY_RIGHT, 0.2)
        elif action == 3:
            press_key(KEY_ACCELERATE, 0.2)
        elif action == 4:
            press_key(KEY_BACKWARDS, 0.2)
        else:
            time.sleep(0.2)

        # Beobachtung
        obs = get_screen()

        # Belohnung: Dummy-Wert (z. B. konstant oder zufällig)
        # => Hier kannst du z. B. Geschwindigkeit via OCR oder Fortschritt später einbauen
        def _compute_reward():
            speed = read_speed()
            return speed / 100.0  # skaliert auf z. B. [0.0 - 3.0]
        
        reward = _compute_reward()
        
        # Spiel vorbei? (Dummy: nie)
        done = False

        return obs, reward, done, {}

# Hauptlauf: Training starten
if __name__ == "__main__":
    env = TrackmaniaEnv()

    model = PPO("CnnPolicy", env, verbose=1)
    model.learn(total_timesteps=10_000)  # Testlauf, später erhöhen

    print("Training abgeschlossen")
