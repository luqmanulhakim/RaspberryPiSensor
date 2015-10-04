from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

LEDPin=22
response= raw_input("Masa untuk set time : ")
checkTime=int(response)
print("your alarm is %s" %response)
# awefeagfae
GPIO.setup(LEDPin, GPIO.OUT)
GPIO.setwarnings(False)
try:
    while True:
        curr_time=int(time.strftime("%H%M"))
        #Print("Curr_time")
        if timenow == checkTime:
            GPIO.output(LEDPin, True)
            print("CEK")
            sleep(2)
        elif currtime != alarm :
            GPIO.output(LEDPin, False)
            print("tak sampai masa lagi")
            sleep(2)
finally:
    #GPI0.cleanup()
    sleep(2)
    
