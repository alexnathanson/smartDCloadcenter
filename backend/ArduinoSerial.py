import serial
import time

print("Arduino Serial connection starting...")

class ArduinoSerial():
    def __init__(self, port):
        self.port = port
        self.baud = 9600
        self.serialObj = serial.Serial(self.port)
        time.sleep(3)

        ReceivedString = self.serialObj.readline()
        print(ReceivedString)
        #self.serialObj.close() 

#arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data

# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value


    def sendByte(self,theByte):
        #with serial.Serial(self.port, self.baud, timeout=1) as ser:
            #time.sleep(0.5)
        #print("byte: " + str(theByte))
        self.serialObj.write(theByte)   # send the pyte string 'H'
            #time.sleep(0.5)   # wait 0.5 seconds
            #ser.write(b'L')   # send the byte string 'L'