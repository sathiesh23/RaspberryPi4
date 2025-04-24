import RPi.GPIO as GPIO
import time

# Pin configuration
RELAY = 25
SWITCH = 4

# Setup
GPIO.setmode(GPIO.BCM)         # Use Broadcom pin numbering
GPIO.setup(RELAY, GPIO.OUT) 
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)  	# Button pin -pull-up resistor

def main():
   while True:
      relay_state = GPIO.input(SWITCH)
      if relay_state == GPIO.LOW:
         GPIO.output(RELAY, 0)			# Activate Relay
         time.sleep(1)
      else:
         GPIO.output(RELAY, 1)			# Deactivate Relay
         time.sleep(0.2)        		

      GPIO.cleanup()				# Cleanup GPIO signals

# Execute the main program
if __name__ == '__main__':
   main()
