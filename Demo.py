import pyfirmata
from random import random
from time import time
import http.client as httplib
import urllib

def thingsSpeak(ldrData):
    
    # use your API key generated in the thingspeak channels for the value of 'key'
    # ldrData is the data you will be sending to the thingspeak channel for plotting the graph. You can add more than one channel and plot more graphs
    params = urllib.parse.urlencode({'field1': ldrData, 'key':'6NXXXXXXXXXXXXXX'})   # Add 'field2': 2ndSensorData and so on if more sensors used
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")                
    try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(response.status, response.reason)
            data = response.read()
            conn.close()
    except:
            print("connection failed")


if __name__ == '__main__':

    board = pyfirmata.Arduino('COM6')                   # The port Arduino board is connected to
    print("Communication Successfully started")
    it = pyfirmata.util.Iterator(board)
    it.start()

    # Analog Pins initialised
    pin_A0 = board.analog[0]
    pin_A0.enable_reporting()

    # Digital pins initialised
    builtIn_Led = board.digital[13]
    count = 0

    while True:                            # Read LDR sensor data every second
        ldrSensorData = pin_A0.read()
        print(ldrSensorData)
        if ldrSensorData:
            if float(ldrSensorData) > 0.6:
                print("Switching on LED")
                builtIn_Led.write(1)
            else:
                print("Switching off LED")
                builtIn_Led.write(0)
                
        count += 1                         # Upload sensor data every 16 seconds by calling thingSpeak function
        if count == 16:
            thingsSpeak(ldrSensorData)
            count = 0

        time.sleep(1)
