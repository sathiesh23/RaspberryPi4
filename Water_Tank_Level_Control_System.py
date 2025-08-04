import RPi.GPIO as GPIO
import time

# Pin configuration
TRIG = 4
ECHO = 17
RELAY = 25

# Tank dimensions (in cm)
TANK_HEIGHT = 500
MIN_LEVEL = 150   # cm from bottom
MAX_LEVEL = 475   # cm from bottom

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.output(RELAY, GPIO.LOW)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance = duration * 17150  	# speed of sound / 2
    return round(distance, 2)

def main():
   while True:
      distance = get_distance()
      for _ in range(50):
         water_level = TANK_HEIGHT - distance
      
      print(f"Water Level: {water_level} cm")

      if water_level < MIN_LEVEL:
         print("Water low ? Pump OFF")
         GPIO.output(RELAY, GPIO.HIGH)
      elif water_level > MAX_LEVEL:
         print("Water high ? Pump ON")
         GPIO.output(RELAY, GPIO.LOW)

      time.sleep(2)


# Execute the main program
if __name__ == '__main__':
   main()

