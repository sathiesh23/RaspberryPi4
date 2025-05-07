import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)					# IC Pin
GPIO.setup(17, GPIO.OUT)				# Servo Motor pin - pull-up resistor
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  	# Switch pin - pull-up resistor


# Create PWM instance on GPIO17 at 50Hz (standard for servos)
pwm = GPIO.PWM(17, 50)
pwm.start(0)

def set_value(value):
    duty = 2 + (value / 18)		# To convert degrees (0 to 180) to duty cycle (2 % to 12 %)
    GPIO.output(17, True)
    pwm.ChangeDutyCycle(duty)		# Set the duty cycle
    time.sleep(0.5)
    GPIO.output(17, False)
    pwm.ChangeDutyCycle(0)		# To avoid jitters in movement

def main():
   while True:
      swt_state = GPIO.input(5)
      if swt_state == GPIO.LOW:		# If switch is pressed activate Servo motor
         set_value(54)			# for -90 degree = 1 ms
         time.sleep(1)
         set_value(99)			# for 0 degree = 1.5 ms
         time.sleep(1)
         set_value(144)			# for +90 degree = 2 ms
         time.sleep(1)
      else:
         pwm.stop()			# If switch is not pressed - stop Servo motor
         GPIO.cleanup()

# Execute the main program
if __name__ == '__main__':
   main()

