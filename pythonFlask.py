from flask import Flask
import RPi.GPIO as GPIO
import time
import math
from ADCDevice import *

adc = ADCDevice() # Define an ADCDevice class object

def setup():
     global adc
     if(adc.detectI2C(0x48)): # Detect the pcf8591.
         adc = PCF8591()
     elif(adc.detectI2C(0x4b)): # Detect the ads7830
         adc = ADS7830()
     else:
         print("No correct I2C address found, \n"
         "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
         "Program Exit. \n");
         exit(-1)

app = Flask(__name__)
@app.route('/')
def index():
         value = adc.analogRead(0)        # read ADC value A0 pin
         voltage = value / 255.0 * 3.3        # calculate voltage
         Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
         tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
         tempC = tempK -273.15        # calculate temperature (Celsius)
         strTemp = str(round(tempC,2))
         temp = "Current temperature: {} degrees C".format(strTemp)
         return temp



if __name__ == '__main__':
     setup()
     app.run(debug=True, port=80, host='0.0.0.0')

