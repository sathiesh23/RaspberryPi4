# Processor: RPI4
# Compiler:  Python 3 (Proteus)
# Modules
from goto import *
import time
import RPi.GPIO as GPIO
led = 7
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
# Main function
def main () :
# Infinite loop
   while 1 :
      GPIO.output(led, GPIO.HIGH)
      time.sleep(1)
      GPIO.output(led, GPIO.LOW)
      time.sleep(1)
 # Command line execution
if __name__ == '__main__' :
   main()