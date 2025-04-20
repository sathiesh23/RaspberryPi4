import RPi.GPIO as GPIO
import time

# GPIO pin setup
IN1 = 17
IN2 = 18
EN_PWM = 27  					
SWT_1 = 5
SWT_2 = 12

GPIO.setmode(GPIO.BCM)			# IC Pins
GPIO.setup(IN1, GPIO.OUT)		# GPIO17 as Output Pin
GPIO.setup(IN2, GPIO.OUT)		# GPIO18 as Output Pin
GPIO.setup(EN_PWM, GPIO.OUT)	# GPIO27 as Output Pin
GPIO.setup(SWT_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO5 as Input Pin, Button pin -pull-up resistor
GPIO.setup(SWT_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO12 as Input Pin, Button pin -pull-up resistor

pwm = GPIO.PWM(EN_PWM, 1000)  	# 1kHz PWM frequency

def motor_forward():
   GPIO.output(IN1, GPIO.HIGH)
   GPIO.output(IN2, GPIO.LOW)

def motor_backward():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.HIGH)

def motor_stop():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)

def main():
   while True:
      state_1=GPIO.input(SWT_1)	# Get the status of GPIO5
      state_2=GPIO.input(SWT_2)	# Get the status of GPIO12
      if(state_1==GPIO.HIGH) and (state_2==GPIO.HIGH):
         pwm.stop()  			# Motor stop
      elif (state_1==GPIO.LOW) and (state_2==GPIO.HIGH):
         pwm.start(20)			# 20% duty cycle
      elif (state_1==GPIO.HIGH) and (state_2==GPIO.LOW):
         pwm.start(60)			# 60% duty cycle 
      else:
         pwm.start(100)			# 100% duty cycle (full speed)
		
      print("DC Motor - Clockwise")
      motor_forward()
      time.sleep(5)
      GPIO.cleanup()

      print("DC Motor - Stop")
      motor_stop()
      time.sleep(2)
      GPIO.cleanup()

      print("DC Motor - AntiClockwise")
      motor_backward()
      time.sleep(5)
      GPIO.cleanup()

      print("DC Motor - Stop")
      motor_stop()
      time.sleep(2)
      GPIO.cleanup()

if __name__ == '__main__' :
   main()
