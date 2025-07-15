import RPi.GPIO as GPIO
import time

# Pin definitions
BUTTON_PIN = 17  	# External interrupt
LED_PIN = 18    	# LED output

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up for button
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Interrupt callback function
def button_callback():
   print("Interrupt detected on GPIO17")
   GPIO.output(LED_PIN, GPIO.HIGH)
   time.sleep(1)
   GPIO.output(LED_PIN, GPIO.LOW)
   time.sleep(1)

# Add interrupt event
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=500)

def main():
   print("Running... Press button connected to GPIO17")
   while True:
      GPIO.output(LED_PIN, GPIO.LOW)
      time.sleep(1)
      
# Execute the main program
if __name__ == '__main__':
   main()

