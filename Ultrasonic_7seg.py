import RPi.GPIO as GPIO
import time

# Pin setup
TRIG = 5
ECHO = 6
segment_pins = [4, 17, 18, 27, 22, 23, 24]  # a,b,c,d,e,f,g
digit_pins = [20, 26, 21]  # For 3-digit control

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
for segment in segment_pins:
   GPIO.setup(segment, GPIO.OUT)
   GPIO.output(segment, 0)
for digit in digit_pins:
   GPIO.setup(digit, GPIO.OUT)
   GPIO.output(digit, 0)

# Digit to segment mapping
segment_map = {
   '0': [1,1,1,1,1,1,0],
   '1': [0,1,1,0,0,0,0],
   '2': [1,1,0,1,1,0,1],
   '3': [1,1,1,1,0,0,1],
   '4': [0,1,1,0,0,1,1],
   '5': [1,0,1,1,0,1,1],
   '6': [1,0,1,1,1,1,1],
   '7': [1,1,1,0,0,0,0],
   '8': [1,1,1,1,1,1,1],
   '9': [1,1,1,1,0,1,1],
}

def measure_distance():
   GPIO.output(TRIG, False)
   time.sleep(0.05)
   GPIO.output(TRIG, True)
   time.sleep(0.00001)
   GPIO.output(TRIG, False)

   while GPIO.input(ECHO)==0:
      pulse_start = time.time()
   while GPIO.input(ECHO)==1:
      pulse_end = time.time()
    
   pulse_duration = pulse_end - pulse_start
   distance = pulse_duration * 17150
   distance = round(distance)
   return distance

def display_number(number):
   print("Distance:", number, "cm")
   str_num = str(number).rjust(3)
   print(f"'{str_num}'")
   for i in range(3):
      if i==0:
         GPIO.output(digit_pins[0], 0)
         GPIO.output(digit_pins[1], 1)
         GPIO.output(digit_pins[2], 1)
      elif i==1:
         GPIO.output(digit_pins[0], 1)
         GPIO.output(digit_pins[1], 0)
         GPIO.output(digit_pins[2], 1)
      elif i==2:
         GPIO.output(digit_pins[0], 1)
         GPIO.output(digit_pins[1], 1)
         GPIO.output(digit_pins[2], 0)
      for j in range(3):
         if j==i:
            for pin, val in zip(segment_pins, segment_map.get(str_num[j], [0]*7)):
               GPIO.output(pin, val)
      time.sleep(0.01)      
 
def main():
   while True:
      dist = measure_distance()
      for _ in range(50):
         display_number(dist)
         time.sleep(0.05)   

# Execute the main program
if __name__ == '__main__':
   main()
