import gym
import numpy as np
import time
import cv2
import mss
from pynput.keyboard import Controller
import pygetwindow as gw
from stable_baselines3 import PPO
import pytesseract
import pyautogui

# === Pixelüberwachung ===
PIXEL_POSITIONS = [(390, 160)]  # Beispiel: Bildschirmmitte
TARGET_COLOR = [0, 0, 0]        # Schwarz
TOLERANCE = 10                  # Farbtoleranz

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

#Bildschirmfarbe an Pixel prüfen
def is_black(pixel):
    return all(abs(pixel[i] - TARGET_COLOR[i]) <= TOLERANCE for i in range(3))

def get_pixel_color(x, y):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))
        pixel = screenshot[y, x, :3]
        return pixel

def check_pixels_and_click():
    for (x, y) in PIXEL_POSITIONS:
        pixel = get_pixel_color(x, y)
        if is_black(pixel):
            pyautogui.click()
            time.sleep(0.5)

#RL-Umgebung definieren
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
        
        reward = 1
        
        # Spiel vorbei? (Dummy: nie)
        done = False

        return obs, reward, done, {}

# Hauptlauf: Training starten
if __name__ == "__main__":
    env = TrackmaniaEnv()

    model = PPO("CnnPolicy", env, verbose=1)
    model.learn(total_timesteps=10_000)  # Testlauf, später erhöhen

    print("Training abgeschlossen")
