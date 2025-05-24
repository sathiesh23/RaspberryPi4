import RPi.GPIO as GPIO
import time
import random

# GPIO pin mapping
LED_PINS = [4, 17, 18, 27, 22, 23, 24]  # L1-L7
BUTTON_PIN = 5

# LED patterns for dice faces 1-6
DICE_FACES = [
    [0,0,0,0,1,0,0],   # 1: Only center
    [1,0,0,0,0,0,1],   # 2: Opposite corners
    [1,0,0,0,1,0,1],   # 3: Two corners + center
    [1,1,0,0,0,1,1],   # 4: Four corners
    [1,1,0,0,1,1,1],   # 5: Four corners + center
    [1,1,1,1,0,1,1],   # 6: All except center column
]

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in LED_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def display_dice(number):
    pattern = DICE_FACES[number-1]
    for i, val in enumerate(pattern):
        GPIO.output(LED_PINS[i], val)

def clear_leds():
    for pin in LED_PINS:
        GPIO.output(pin, 0)

def main():
    setup()
    print("Press the button to roll the dice!")
    try:
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                roll = random.randint(1, 6)
                print(f"Dice Rolled: {roll}")
                display_dice(roll)
                time.sleep(1.5)
                clear_leds()
                # Wait until button is released to avoid double roll
                while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    time.sleep(0.1)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
