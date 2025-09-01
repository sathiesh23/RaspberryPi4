import RPi.GPIO as GPIO
import time

IR_PIN = 17      # IR sensor D0 pin
LED_PIN = 27     # LED pin (with 330O resistor)

GPIO.setmode(GPIO.BCM)
# sensor usually active-LOW
GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(LED_PIN, GPIO.OUT, initial = GPIO.LOW)

try:
    while True:
        if GPIO.input(IR_PIN) == GPIO.LOW:   # Object detected
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
        else:
            GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED OFF
        time.sleep(0.05)  # small delay to avoid CPU load
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()
