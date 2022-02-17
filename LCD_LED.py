
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import threading
from time import sleep, strftime
from datetime import datetime

import RPi.GPIO as GPIO
import time
from flask import Flask

pins = [11, 12, 13]         # define the pins for R:11,G:12,B:13 


def setup():
    global pwmRed,pwmGreen,pwmBlue  
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(pins, GPIO.OUT)     # set RGBLED pins to OUTPUT mode
    GPIO.output(pins, GPIO.HIGH)   # make RGBLED pins output HIGH level
    pwmRed = GPIO.PWM(pins[0], 2000)      # set PWM Frequence to 2kHz
    pwmGreen = GPIO.PWM(pins[1], 2000)  # set PWM Frequence to 2kHz
    pwmBlue = GPIO.PWM(pins[2], 2000)    # set PWM Frequence to 2kHz
    pwmRed.start(0)      # set initial Duty Cycle to 0
    pwmGreen.start(0)
    pwmBlue.start(0)
    
def setColor(r_val,g_val,b_val):      # change duty cycle for three pins to r_val,g_val,b_val
    pwmRed.ChangeDutyCycle(r_val)     # change pwmRed duty cycle to r_val
    pwmGreen.ChangeDutyCycle(g_val)   
    pwmBlue.ChangeDutyCycle(b_val)

def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 )
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    

def loop():
    while True:
        mcp.output(3,1)     # turn on LCD backlight
        lcd.begin(16,2)     # set number of LCD lines and columns
        
        #lcd.clear()
        value = float(get_cpu_temp())
        lcd.setCursor(0,0)  # set cursor position
        lcd.message( 'CPU: ' + str(value) + ' C' + '\n' )# display CPU temperature
        lcd.message( get_time_now() )   # display the time
        
        #changes led colour depending on temperature
        if value <= 45:
            setColor(100,75,25)
        elif value <= 50:
            setColor(100,50,50)
        elif value <= 55:
           setColor(50,50,100)
        elif value <=60:
            setColor(25,75,100)
        else:
            setColor(0,100,100)
        
        sleep(1)
    
        
        
def destroy():
    pwmRed.stop()
    pwmGreen.stop()
    pwmBlue.stop()
    GPIO.cleanup()   
    lcd.clear()
 
 
app = Flask(__name__)
@app.route('/')  
def webServer():
    time = datetime.now().strftime('    %H:%M:%S')
    temp = get_cpu_temp()
    cpuTemp = str(temp) + ' C'
     
    global string
    string = 'Time: ' + time + ' | ' + 'CPU Temperature: ' + cpuTemp
    
    return string


def runServer():
    app.run(debug=False, port=80, host='0.0.0.0', threaded = True)
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    setup()

    try:
      #sets up threads to run the webserver and lcd screen in parallel
        first_thread = threading.Thread(target=loop)
        second_thread = threading.Thread(target=runServer)
        second_thread.start()
        first_thread.start()

            

    except KeyboardInterrupt:
        destroy()
