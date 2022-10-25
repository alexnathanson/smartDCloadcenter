#import threading
#import logging
import api

#this is the code for communicating with an Arduino via serial
from arduinoSerial import ArduinoSerial as Arduino 

def arduinoSerialCommunication():
	try:
		arduino = Arduino('COM8')
		arduino.readThread.start()

	except Exception as e:
		print(e)

	except KeyboardInterruption:
		pass

def runAll():

    arduinoSerialCommunication()
    api.app.run()



if __name__ == '__main__':
 
    runAll()