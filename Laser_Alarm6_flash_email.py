# Laser Tripwire Alarm with Raspcontroller App and Email Alerts
# Written By Gary Jefferson
# RC time constant Reference: https://pimylifeup.com/raspberry-pi-light-sensor/
# Code Logic Reference: https://www.youtube.com/watch?v=4oJiXlPs46o
# Email Reference: https://www.youtube.com/watch?v=sLjqrXvZvfk&t=311s

import RPi.GPIO as GPIO
import time
import smtplib
from gpiozero import LightSensor, Buzzer, LED
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)    #laser on GPIO 22
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT) 

# ldr = LightSensor(4)
buzzer = Buzzer(17)
red_led = LED(27)
green_led = LED(23)
flash = LED(24)

#Arm/Disarm using GPIO Controll on App
GPIO.output(22, False)#laser off
GPIO.output(12, False)#green1 off
GPIO.output(13, False)#yellow off
GPIO.output(6, False)#green2 off
GPIO.output(5, False)#green3 off
green_led.off()#green LED turn on  to show the code is running   

#set up email info
#sender email info (less secure app access required)
smtpUser = '*********@gmail.com'    #sender email address
smtpPass = '********'               #sender email password

#reciever email info
toAdd = 'jose.garza@sjsu.edu'
fromAdd = smtpUser

#type in the subject
subject = 'Security Alarm Activated'
#header for printing in terminal
header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
#type in the body of the email (your message)
body = 'Intruder Detected!'
#display in terminal
print(header + '\n' + body)

def email (smtpUser, smtpPass, fromAdd, toAdd, header, body):
    #establishing connection with email server (gmil.com) 
    s = smtplib.SMTP('smtp.gmail.com',587)
    #synchronizing connections
    s.ehlo()
    s.starttls()
    s.ehlo()
    #logging in
    s.login(smtpUser, smtpPass)
    print('login successfull')
    #send email after successfull login
    s.sendmail(fromAdd, toAdd, header + '\n\n' + body)
    s.quit()

#define the pin that goes to the circuit
pin_to_circuit = 4

def flasher (flash):        #function to controll flashing
    while GPIO.input(22):   #while laser is on
        flash.on()
        time.sleep(.1)
        flash.off()
        time.sleep(.1)
        
 
def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.001)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        if (GPIO.input(22) and not GPIO.input(27)):
            green_led.on()    #Green LED on if laser is on (armed)
        else:
            green_led.off()
        while GPIO.input(22): #while laser on
            if (GPIO.input(22) and not GPIO.input(27)):
                green_led.on()    #Green LED on if laser is on (armed)
            if rc_time(pin_to_circuit) > 5000 :    #if light sensitivity drops below threshold (10000 - 33000)
                buzzer.on()
                red_led.on() #LED stays on if activated
                green_led.off()
                email (smtpUser, smtpPass, fromAdd, toAdd, header, body)  #calls email function
                #additional reciever email info
                toAdd = 'gary.jefferson@sjsu.edu'
                #sends second email to additional address
                email (smtpUser, smtpPass, fromAdd, toAdd, header, body)  #calls email function
                flasher(flash)   #calls flash function
            if not(GPIO.input(22)): #turn off LED when disarmed
                red_led.off()
                buzzer.off()
                #green_led.on()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
