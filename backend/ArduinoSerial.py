import serial
import threading
import time
import sys
import signal
import requests
#import json

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
        self.readThread = threading.Thread(target=self.readLoop) #make this a daemon!!!
        #branch state is whether it is currently on or off, branch status is whether it is a critical or shedable
        self.data = {"system":{"modules":0,"loadBranches":3,"branchState":{1:0,2:0,3:0}},
                    "pv":{"current":0,"voltage":0,"power":0},
                    "load":{"current":0,"voltage":0,"power":0},
                    }

    def readLoop(self):
        print("starting read loop")

        uI = {"load":
            {"branch1":{"status":0},
            "branch2":{"status":0},
            "branch3":{"status":0}}}

        #try:
        while True:
            if self.serialObj.in_waiting > 0:
                # print("")
                # print(self.serialObj.in_waiting )
                newData = self.serialObj.readline().decode()

                if "modules" in newData:
                    self.data["system"]["modules"]= self.cleanSerial(newData)
                elif "branch1" in newData:
                    self.data["system"]["branchState"][1]= self.cleanSerial(newData)
                elif "branch2" in newData:
                    self.data["system"]["branchState"][2]= self.cleanSerial(newData)
                elif "branch3" in newData:
                    self.data["system"]["branchState"][3]= self.cleanSerial(newData)

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

                #print(self.data)
                elif "******" in newData:
                    postJSON(self.data)
            else:
                newUI = getUserInput()

                #this is stupid...change this to a real thing in the future...

                if newUI != uI:
                    
                    print(uI)


                    if uI['load']['branch1']['status']!= newUI['load']['branch1']['status']:
                        self.sendByte('A')
                    
                    if uI['load']['branch2']['status']!= newUI['load']['branch2']['status']:
                        self.sendByte('S')
                    elif uI['load']['branch3']['status']!= newUI['load']['branch3']['status']:
                        self.sendByte('D')
                    #sendByte(uI['branch'] + ":" + uI['status'])
                    uI = newUI

            time.sleep(0.05)
            # if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            #     print('You Pressed A Key!')
            #     break  # finishing the loop
        # except KeyboardInterrupt:
        #     pass

    def sendByte(self,theByte):
        #with serial.Serial(self.port, self.baud, timeout=1) as ser:
            #time.sleep(0.5)
        #print("byte: " + str(theByte))
        self.serialObj.write((bytes(theByte, 'utf-8')))   # send the pyte string 'H'
            #time.sleep(0.5)   # wait 0.5 seconds
            #ser.write(b'L')   # send the byte string 'L'


    def cleanSerial(self, rawData):
        #split on ':' delineator, remove white spaces and line breaks
        cleanedData = rawData.split(":")[1].replace(" ", "").rstrip()
        return cleanedData

def getUserInput():
    try:
        return requests.get('http://localhost:5000/api?data=user').json()
    except:
        print(requests.exceptions)

def postJSON(dstData):
    try:
        headers = {'Content-type': 'application/json'}
        x = requests.post('http://localhost:5000/api', headers=headers,json = dstData, timeout=5)
        # if x.ok:
        #     try:
        #         print("Post successful")
        #     except:
        #         print("Malformatted response")
        #         print(x.text)
        #requests.raise_for_status()
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error", e)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

if __name__ == '__main__':

    arduino = ArduinoSerial('COM8')
    arduino.readThread.start()