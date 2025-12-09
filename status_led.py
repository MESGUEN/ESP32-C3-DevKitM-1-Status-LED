# status_led.py
# Control the ESP32-C3-DevKitM-1 onboard RGB LED (WS2812 on GPIO 8)
#
# Ce module fournit des fonctions simples pour :
# - allumer la LED dans différentes couleurs (rouge, vert, bleu, blanc),
# - régler la luminosité en pourcentage (0–100 %),
# - éteindre la LED.
#
# Exemple d'utilisation:
#
# from status_led import StatusLed 
#
# led = StatusLed(brightness=20)  # création de l'objet led avec 20 % de luminosité
#
# led.red()         
# led.green()
# led.blue()
# led.yellow()
# led.magenta()
# led.cyan()
# led.set_brightness(50)
# led.white()  # blanche à 50%
# led.off()
#
# led.blink(255, 0, 0, delay=0.1, count=3)   # clignotement rouge de 3 fois 0.1s
# led.pulse(0, 0, 255)                       # effet "respiration" bleu


from machine import Pin
import neopixel
import time


class StatusLed:
    def __init__(self, pin=8, n=1, brightness=20):
        """
        pin        : GPIO used for the WS2812 data line (8 on ESP32-C3-DevKitM-1)
        n          : number of LEDs in the chain (1 for onboard LED)
        brightness : global brightness in percent (0–100), e.g. 20 = 20%
        """
        self.np = neopixel.NeoPixel(Pin(pin), n)
        self.set_brightness(brightness)
        self.off()

    def set_brightness(self, brightness_percent):
        """Set global brightness in percent (0–100)."""
        if brightness_percent < 0:
            brightness_percent = 0
        if brightness_percent > 100:
            brightness_percent = 100
        # store as factor 0.0–1.0
        self.brightness = brightness_percent / 100.0

    def _scale(self, v):
        # v in 0–255 → apply brightness factor 0.0–1.0
        v = max(0, min(255, int(v)))
        return int(v * self.brightness)

    def _set(self, r, g, b):
        self.np[0] = (self._scale(r), self._scale(g), self._scale(b))
        self.np.write()

    # Couleurs fixes

    def off(self):
        self._set(0, 0, 0)

    def red(self):
        self._set(255, 0, 0)

    def green(self):
        self._set(0, 255, 0)

    def blue(self):
        self._set(0, 0, 255)

    def yellow(self):
        self._set(255, 255, 0)

    def magenta(self):
        self._set(255, 0, 255)

    def cyan(self):
        self._set(0, 255, 255)

    def white(self):
        """White (R+G+B)."""
        self._set(255, 255, 255)

    # Effets simples

    def blink(self, r, g, b, delay=0.2, count=5):
        """
        Blink a given color (r, g, b in 0–255).
        delay : time in seconds between ON/OFF.
        count : number of blinks.
        """
        for _ in range(count):
            self._set(r, g, b)
            time.sleep(delay)
            self.off()
            time.sleep(delay)

    def pulse(self, r, g, b, steps=20, delay=0.05):
        """
        Simple breathing / pulse effect using the current brightness
        as maximum level.
        """
        max_brightness = self.brightness if self.brightness > 0 else 1.0

        # fade in
        for i in range(steps + 1):
            level = max_brightness * (i / steps)
            old = self.brightness
            self.brightness = level
            self._set(r, g, b)
            self.brightness = old
            time.sleep(delay)

        # fade out
        for i in range(steps, -1, -1):
            level = max_brightness * (i / steps)
            old = self.brightness
            self.brightness = level
            self._set(r, g, b)
            self.brightness = old
            time.sleep(delay)

        self.off()


