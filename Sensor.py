this is all coding for the program
import spidev
from time import sleep
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
# first open up SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# initialize what sensor is where
lightChannel = 0
tempChannel = 1
sleepTime = 3
LEDPin=22

# setup the LED, dummy before replace with triggering email action
GPIO.setup(LEDPin, GPIO.OUT)


def getReading(channel):
    # first pull the rawdata from the chip
    rawData = spi.xfer([1, (8 + channel) << 4, 0])

    #process the raw data into something we understand
    processedData = ((rawData[1]&3) << 8) + rawData[2]
    return processedData

def convertVoltage(bitValue, decimalPlaces=2):
    voltage = (bitValue * 3.3)/float(1023)
    voltage = round(voltage, decimalPlaces)
    return voltage

def convertTemp(bitValue, decimalPlaces=2):
    # converts to degree Celcius
    temperature1 = ( (bitValue * 3.3)/float(1023))
    temperature2 = temperature1/(10.0/1000) #because lm35 output is 10mV per degree
    temperature2 = round(temperature2, decimalPlaces)
    return temperature2

try:
    #while True:
    lightData = getReading(lightChannel)
    tempData = getReading(tempChannel)
    lightVoltage = convertVoltage(lightData)
    tempVoltage = convertVoltage(tempData)
    temperature2 = convertTemp(tempData)
    #print("light bitValue = {} ; Voltage {}". format(lightData, lightVoltage))
    #print("Temp bitValue = {} ; Voltage = {} V; Temp {} C".format(tempData, tempVoltage, temperature2))
    if lightVoltage <= 2.7 and temperature2 <= 25 :
        print("LAMP AND AIRCOND STILL NOT TURN OFF")
        print("Temp bitValue = {} ; Voltage = {} V; Temp {} C".format(tempData, tempVoltage, temperature2))
        print("light bitValue = {} ; Voltage {}". format(lightData, lightVoltage))
        GPIO.output(LEDPin, True)
        sleep(sleepTime)
    if lightVoltage > 2.7 and temperature2 > 30:
        print("LAMP and AIRCOND already shut off")
        GPIO.output(LEDPin, False)
        sleep(sleepTime)
    if lightVoltage < 2.7 and temperature2 > 30:
        print("LAMP not turn Off")
        print("light bitValue = {} ; Voltage {}". format(lightData, lightVoltage))
        GPIO.output(LEDPin, True)
        sleep(sleepTime)
    elif lightVoltage >2.7 and temperature2 < 30:
        print("Temp bitValue = {} ; Voltage = {} V; Temp {} C".format(tempData, tempVoltage, temperature2))
        print("Aircond not turn off")
        GPIO.output(LEDPin, True)
        sleep(sleepTime)
finally:
    GPIO.cleanup()
        
