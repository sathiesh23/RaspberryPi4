import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 5		# GPIO 5
LCD_E  = 6		# GPIO 6
LCD_D4 = 12		# GPIO 12
LCD_D5 = 13		# GPIO 13
LCD_D6 = 16		# GPIO 16
LCD_D7 = 19		# GPIO 19

LCD_WIDTH = 16     # Max characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for line 1
LCD_LINE_2 = 0xC0  # LCD RAM address for line 2

E_PULSE = 0.0005   # 500 us
E_DELAY = 0.0005   # 500 us

def lcd_config():
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BCM) 		# Configuring Board Pins
   GPIO.setup(LCD_E, GPIO.OUT)	# Configuring GPIO pins as Output Port Pins
   GPIO.setup(LCD_RS, GPIO.OUT)
   GPIO.setup(LCD_D4, GPIO.OUT)
   GPIO.setup(LCD_D5, GPIO.OUT)
   GPIO.setup(LCD_D6, GPIO.OUT)
   GPIO.setup(LCD_D7, GPIO.OUT)

def lcd_init():
   lcd_byte(0x33, LCD_CMD)	# LCD Display in 8-bit Mode
   lcd_byte(0x32, LCD_CMD)	# Transitioning into 4-bit Mode
   lcd_byte(0x28, LCD_CMD)	# Sets the LCD to a 4-bit data
   lcd_byte(0x0C, LCD_CMD)	# Turn the display ON and disable the cursor
   lcd_byte(0x06, LCD_CMD)	# Sets the entry mode to auto-increment cursor
   lcd_byte(0x01, LCD_CMD)	# clears the entire display on an LCD
   time.sleep(E_DELAY)

# Sending signals to LCD Pins (4-bit Mode)
def lcd_byte(bits, mode):
   GPIO.output(LCD_RS, mode)

   GPIO.output(LCD_D4, False)
   GPIO.output(LCD_D5, False)
   GPIO.output(LCD_D6, False)
   GPIO.output(LCD_D7, False)
   if bits & 0x10 == 0x10:
      GPIO.output(LCD_D4, True)
   if bits & 0x20 == 0x20:
      GPIO.output(LCD_D5, True)
   if bits & 0x40 == 0x40:
      GPIO.output(LCD_D6, True)
   if bits & 0x80 == 0x80:
      GPIO.output(LCD_D7, True)

   lcd_toggle_enable()

   GPIO.output(LCD_D4, False)
   GPIO.output(LCD_D5, False)
   GPIO.output(LCD_D6, False)
   GPIO.output(LCD_D7, False)
   if bits & 0x01 == 0x01:
      GPIO.output(LCD_D4, True)
   if bits & 0x02 == 0x02:
      GPIO.output(LCD_D5, True)
   if bits & 0x04 == 0x04:
      GPIO.output(LCD_D6, True)
   if bits & 0x08 == 0x08:
      GPIO.output(LCD_D7, True)

   lcd_toggle_enable()

def lcd_toggle_enable():
   time.sleep(E_DELAY)		# 500 us
   GPIO.output(LCD_E, True)	# E = 1
   time.sleep(E_PULSE)		# 500 us
   GPIO.output(LCD_E, False)# E = 0
   time.sleep(E_DELAY)		# 500 us

def lcd_string(message, line):				# Print the messages in LCD
   message = message.center(LCD_WIDTH, " ") # message.ljust(); message.rjust()
   lcd_byte(line, LCD_CMD)
   for i in range(LCD_WIDTH):				# LCD_WIDTH = 16
      # returns the integer representation of the character at index i
      # within the string message.
      lcd_byte(ord(message[i]), LCD_CHR)	# Data is sent - LCD_CHR = True

def main():
   lcd_config()			# GPIO Pin Direction is set
   lcd_init()			# LCD Initialization
   while True:
      lcd_string("Embedded Systems!", LCD_LINE_1)
      lcd_string("Raspberry Pi 4", LCD_LINE_2)

      time.sleep(5)		# 5 seconds

      lcd_string("LCD Interface", LCD_LINE_1)
      lcd_string("4-bit Mode", LCD_LINE_2)

      time.sleep(5)		# 5 seconds
      lcd_byte(0x01, LCD_CMD) # Clear LCD

      GPIO.cleanup()	# Cleanup GPIO signals

# Execute the main program
if __name__ == '__main__':
   main()
