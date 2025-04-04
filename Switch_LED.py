import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 17
BUTTON_PIN = 18

# Setup
GPIO.setmode(GPIO.BCM)         # Use Broadcom pin numbering
GPIO.setup(LED_PIN, GPIO.OUT)  # LED pin as output
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin as input with pull-up resistor

try:
    led_on = False
    while True:
        button_state = GPIO.input(BUTTON_PIN)
        if button_state == GPIO.LOW:  # Button is pressed (connected to GND)
            led_on = not led_on
            GPIO.output(LED_PIN, led_on)
            print(f"LED {'ON' if led_on else 'OFF'}")
            time.sleep(0.3)  # Debounce delay
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting program...")
