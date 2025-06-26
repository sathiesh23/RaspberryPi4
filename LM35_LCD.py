import RPi.GPIO as GPIO
import time

# ADC Control Pins
ale = 2
start = 21
eoc = 7
oe = 3
adc_data_pins = [26, 20, 19, 16, 13, 12, 6, 5]  # D0–D7

# LCD Pins
rs = 18
en = 27
d4, d5, d6, d7 = 22, 23, 24, 25

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Setup ADC GPIO – Data Direction
GPIO.setup(adc_data_pins, GPIO.IN)
GPIO.setup([ale, start, oe], GPIO.OUT)
GPIO.setup(eoc, GPIO.IN)
GPIO.setup([rs, en, d4, d5, d6, d7], GPIO.OUT)

def pulse(pin):				# High to Low Pulse
   GPIO.output(pin, True)
   time.sleep(0.001)		# 1 ms
   GPIO.output(pin, False)

def adc_read():
   GPIO.output(ale, True)	# ale = High to Low Pulse
   time.sleep(0.001)		# 1 ms
   GPIO.output(start, True)# start = High to Low Pulse
   time.sleep(0.001)		# 1 ms
   GPIO.output(ale, False)
   GPIO.output(start, False)

   while GPIO.input(eoc) == 1:	# check for eoc signal
      pass

   GPIO.output(oe, True)	# oe = output enable
   value = 0
   for i in range(8):		# read the adc output
      if GPIO.input(adc_data_pins[i]):
         value |= (1 << i)
   GPIO.output(oe, False)	# oe = output disabled
   return value			# return the adc value

# LCD low-level functions
def lcd_send_nibble(nibble):	# send nibble
   GPIO.output(d4, nibble & 0x01)
   GPIO.output(d5, (nibble >> 1) & 0x01)
   GPIO.output(d6, (nibble >> 2) & 0x01)
   GPIO.output(d7, (nibble >> 3) & 0x01)
   pulse(en)

def lcd_send_byte(value, mode):	# send byte with mode info
   GPIO.output(rs, mode)
   lcd_send_nibble(value >> 4)		# send upper nibble
   lcd_send_nibble(value & 0x0F) 	# send lower nibble
   time.sleep(0.001)			    # 1 ms

def lcd_init():
   lcd_send_byte(0x33, 0)  # LCD Display in 8-bit Mode
   lcd_send_byte(0x32, 0)  # Transitioning into 4-bit Mode
   lcd_send_byte(0x28, 0)  # Sets the LCD to a 4-bit data
   lcd_send_byte(0x0C, 0)  # Display on, cursor off
   lcd_send_byte(0x06, 0)  # Entry mode
   lcd_send_byte(0x01, 0)  # Clear display
   time.sleep(0.01)

def lcd_write(message):
   for char in message:
      lcd_send_byte(ord(char), 1)

def lcd_set_cursor(line):
   addr = 0x80 if line == 1 else 0xC0
   lcd_send_byte(addr, 0)

def main():
   lcd_init()
   while True:
      digital = adc_read()
      voltage = (digital / 255.0) * 5000
      temperature = voltage / 10  # LM35 = 10mV/°C

      lcd_set_cursor(1)
      lcd_write("Temp: {:0.1f} C   ".format(temperature))
      time.sleep(1)
      GPIO.cleanup()

# Execute the main program
if __name__ == '__main__':
   main()

