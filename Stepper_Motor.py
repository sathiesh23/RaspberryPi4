import RPi.GPIO as GPIO
import time

# GPIO pin setup
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Define anti-clockwise sequence
aclk_sequence = [
    [0,1,1,0],
    [0,1,1,1],
    [0,0,1,1],
    [1,0,1,1],
    [1,0,0,1],
    [1,1,0,1],
    [1,1,0,0],
    [1,1,1,0]
]

clk_sequence = [
    [1,1,1,0],
    [1,1,0,0],
    [1,1,0,1],
    [1,0,0,1],
    [1,0,1,1],
    [0,0,1,1],
    [0,1,1,1],
    [0,1,1,0]
]

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  	# Switch pin - pull-up resistor

def move_steps_clk(steps, delay=1):
    for _ in range(steps):
        for step in clk_sequence:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(delay)

def move_steps_aclk(steps, delay=1):
    for _ in range(steps):
        for step in aclk_sequence:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(delay)

def main():
   while True:
      swt_state=GPIO.input(5)
      if swt_state == GPIO.LOW:
         print("Rotating stepper motor... Clockwise")
         move_steps_clk(1)       
         GPIO.cleanup()
      else:
         print("Rotating stepper motor... Anticlockwise")
         move_steps_aclk(1)
         GPIO.cleanup()

# Execute the main program
if __name__ == '__main__':
   main()

