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

ledPin = 23 # Broadcom pin 23 (Pi pin 16)
broker="192.168.12.214"
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
    print("Received: Topic" + msg.topic + " Message: " + msg.payload.decode() )
    dmsg =  msg.payload.decode()
    DoLightBulbCommand(dmsg);

   

try:
    client= paho.Client("control1",transport="websockets");
    # client1.on_publish = on_publish    
    # client1.on_message = on_message;                     #assign function to callback
    client.connect(broker,port)                                 #establish connection
    #ret= client1.publish("smart/bulb","on")  
    client.subscribe("bulb");   
    client.on_message = on_message;
    client.loop_forever();
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
    print("All done! bye!");

