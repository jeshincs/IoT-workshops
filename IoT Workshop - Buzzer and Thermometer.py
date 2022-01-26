import machine
from machine import PWM, Pin
from time import sleep
import dht

def setup():
  print('made it to setup')
  global buzzer
  global sensor
  buzzer =(machine.Pin(14, machine.Pin.OUT)) # define buzzerPin
  sensor = dht.DHT11(Pin(12))

  
def loop():
  print('made it to loop')
  while True:
    try:
      sleep(1)
      sensor.measure()
      temp = sensor.temperature()
      

      if temp > 30:
        print('Temperature: %3.1f C, Temperature above threshold, alarm activated!' %temp)
        buzzer.value(1)
        sleep(1)
        buzzer.value(0)
      else:
        print('Temperature: %3.1f C' %temp)

        
    except OSError as e:
      print('Failed to read sensor.')

def destroy():
  machine.cleanup() # Release all GPIO

if __name__ == '__main__': # Program entrance
  print ('Program is starting...')
  setup()
  try:
    loop()
  except KeyboardInterrupt: # Press ctrl-c to end the program.
    destroy()
