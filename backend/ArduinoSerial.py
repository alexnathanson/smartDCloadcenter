import serial
import threading
import time
import sys
import signal

#this is to exit the loop from the keyboard
# def signal_handler(signal, frame):
#     print("\nprogram exiting gracefully")
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

print("Arduino serial connection starting...")

class ArduinoSerial():
    def __init__(self, port):
        self.port = port
        self.baud = 9600
        self.serialObj = serial.Serial(self.port)
        self.readThread = threading.Thread(target=self.readLoop)
        #self.readThread.start()
        self.data = {"system":{"modules":0},
                    "pv":{"current":0,"voltage":0,"power":0},
                    "load":{"current":0,"voltage":0,"power":0}
                    }
        self.dateFile = "/data/ardiono.txt"
        # ReceivedString = self.serialObj.readline()
        # print(ReceivedString.decode())
        #self.serialObj.close() 

    def readLoop(self):
        print("starting read loop")

        while True:
            if self.serialObj.in_waiting > 0:
                newData = self.serialObj.readline().decode()

                if "modules" in newData:
                    self.data["system"]["modules"]= self.cleanSerial(newData)
                elif "pv voltage" in newData:
                    self.data["pv"]["voltage"]= self.cleanSerial(newData)
                elif "pv current" in newData:
                    self.data["pv"]["current"]= self.cleanSerial(newData)
                elif "pv power" in newData:
                    self.data["pv"]["power"]= self.cleanSerial(newData)
                elif "load voltage" in newData:
                    self.data["load"]["voltage"]= self.cleanSerial(newData)
                elif "load current" in newData:
                    self.data["load"]["current"]= self.cleanSerial(newData)
                elif "load power" in newData:
                    self.data["load"]["power"]= self.cleanSerial(newData)
                print(self.data)
                time.sleep(0.05)

    def sendByte(self,theByte):
        #with serial.Serial(self.port, self.baud, timeout=1) as ser:
            #time.sleep(0.5)
        #print("byte: " + str(theByte))
        self.serialObj.write(theByte)   # send the pyte string 'H'
            #time.sleep(0.5)   # wait 0.5 seconds
            #ser.write(b'L')   # send the byte string 'L'


    def cleanSerial(self, rawData):
        #split on ':' delineator, remove white spaces and line breaks
        cleanedData = rawData.split(":")[1].replace(" ", "").rstrip()
        return cleanedData

if __name__ == '__main__':

    arduino = ArduinoSerial('COM8')
    arduino.readThread.start()