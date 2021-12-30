# Laser-Alarm

In order to run the code sucessfully, the circuit muust be built according to the schematic.
This program is activated using the Raspcontroller App by turning on (setting to 1) GPIO 22. Gpio 22 is the arm/disarm pin which is controlled via the app.
The program will then: turn on buzzer, turn on Red LED, send an email (or 2) followed by entering a loop that flashes the strobe lights. 
The strobe lights will continue to flash untill GPIO is turned off (setting to 0).
The sensitivity of the laser alarm is adjusted by the following line of code:

        if rc_time(pin_to_circuit) > 5000 :
    
The threshold is currently set to 5000 for a quick responce to fast motion. A smaller number will yield a quicker responce but is subject to false alarms on occation.
A larger number will allow very fast motions to go undetected. I found that a threshold number between 5000 - 33000 works best.

Email:
There is a sending email address that you will need to provide along with the sending email password. 
It is marked with asterisks since you can put what ever email and password you like. 
*Keep in mind that the sending email address needs to allow *less secure app access* which you will need to change the settings in your gmail account.
Then you can change the recieving email address to your email address (does not need less secure app access).


References:

[1] https://www.youtube.com/watch?v=4oJiXlPs46o

[2] https://pimylifeup.com/raspberry-pi-light-sensor/

[3] https://www.youtube.com/watch?v=sLjqrXvZvfk&t=311s
