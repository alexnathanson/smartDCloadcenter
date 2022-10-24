#import threading
#import logging
import api
import json

#this is the code for communicating with an Arduino via serial
from arduinoSerial import ArduinoSerial as Arduino 

def flaskServer():
 	api.app.run()

def arduinoSerialCommunication():
	try:
		arduino = Arduino('COM8')
		arduino.readThread.start()

	except Exception as e:
		print(e)

	except KeyboardInterruption:
		pass

def runAll():

    # flaskThread = thread.Thread(target=flaskServer, daemon=True)
    # arduinoThread = thread.Thread(target=arduinoSerialCommunication, daemon=True)

    # flaskThread.start()
    arduinoSerialCommunication()
    api.app.run()


if __name__ == '__main__':
 
    runAll()