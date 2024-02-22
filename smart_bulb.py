# tutorial reference: http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
# http://www.steves-internet-guide.com/mqtt-websockets/


# prereqs: ssh to the raspberry pi
#pi@ip_address

# use paho mqtt client to to control circuit
# 1. install Paho MQTT client: 
# pip3 install paho-mqtt

# 2. use RPi.GPIO https://pypi.org/project/RPi.GPIO/
# https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-example
# pip3 install RPi.GPIO


# secure copy python script to Raspberry Pi
# scp .\smart_bulb.py username@ip-address:~/smart_bulb


import RPi.GPIO as GPIO
import paho.mqtt.client as paho

import string
import random

ledPin = 23  #Broadcom pin 23 (Pi pin 16)
broker="127.0.0.1"
port=9001

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
# Initial state for LEDs:
GPIO.output(ledPin, GPIO.LOW)


def DoLightBulbCommand(cmd):
    if cmd == "on":
        GPIO.output(ledPin, GPIO.HIGH);
    else:
        GPIO.output(ledPin, GPIO.LOW);

    
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n");
    pass


def on_message(client,userdata,msg):
    print("Received Topic: " + msg.topic + " Message: " + msg.payload.decode() )
    dmsg =  msg.payload.decode()
    DoLightBulbCommand(dmsg);

   
def GetName(N):
    # N = size of string
    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=N))
    return res



def on_connect_fail(msg):
     print("Could not connect to MQTT Broker at " + broker + ":" + port);


def on_connect(client, userdata, flags, rc):
    print("Python Client connected over web sockets with result: " + str(rc));
    
    subscription1 = "bulb"
    client.subscribe(subscription1);     
    print("Subscribed to topic: " + subscription1);



try:
    client_name = GetName(10) +"_client"
    client= paho.Client(client_name,transport="websockets")
             
    client.connect(broker,port)   #establish connection
    print("client " + client_name)
   
    client.on_message = on_message;  #assign function to callback
    client.on_connect = on_connect; 
    client.on_connect_fail = on_connect_fail;
    client.loop_forever();

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
    print("All done! bye!");

