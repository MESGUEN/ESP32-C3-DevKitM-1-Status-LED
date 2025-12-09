# ESP32-C3-DevKitM-1-Status-LED
This module controls the ESP32-C3-DevKitM-1 onboard RGB LED (WS2812 on GPIO 8). It provides simple functions and a class to set colors, turn the LED on or off, and create visual effects like blinking or pulsing.
## Installation
1. Download `status_led.py`
2. Copy it to the ESP32-C3 flash memory (root '/' or folder `/lib`)

## Example
```python
from status_led import StatusLed

led = StatusLed()   # GPIO 8 par défaut sur la DevKitM-1

led.red()           # la LED doit devenir rouge
led.green()
led.blue()
led.off()

led.blink(255, 0, 0, delay=0.1, count=3)   # clignotement rouge
led.pulse(0, 0, 255)                       # effet "respiration" bleu
