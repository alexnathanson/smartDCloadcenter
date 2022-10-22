/*
  Decentralized Emergent Energy System (D.E.E.S)
  October 21, 2022

  INA219 code based on the Adafruit INA219 getcurrent example
  https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout
 */

#include <Wire.h>
#include <Adafruit_INA219.h>

//A4 & A5 are the I2C pins that read INA219 current and voltage sensor
Adafruit_INA219 ina219_PV; // defaults to 0x40
Adafruit_INA219 ina219_LOAD(0x41);

bool ina_pv_status = false;
bool ina_load_status = false;

//these pins control load MOSFETs
const int load1 = 2;
const int load2 = 3;
const int load3 = 4;

//these pins control PV input relays (NOT BEING USED CURRENTLY
//const int pv = 6;

//this pin is the PV reed switch
const int rs =7;
int rState = 0;

// the setup function runs once when you press reset or power the board
void setup() {

  //original code this was based on used 115200 baud, not sure if that is the INA219 spec or arbitrary
  Serial.begin(9600);

  //remove?
  while (!Serial) {
      // will pause Zero, Leonardo, etc until serial console opens
      delay(1);
  }

   uint32_t currentFrequency;

  // Initialize the INA219.
  // By default the initialization will use the largest range (32V, 2A).  However
  // you can call a setCalibration function to change this range (see comments).
  if (! ina219_PV.begin()) {
    Serial.println("Failed to find INA219 PV chip");
    //while (1) { delay(10); }
     ina_pv_status = false;
  } else {
    Serial.println("INA219 PV chip found");
    ina_pv_status = true;
  }

   if (! ina219_LOAD.begin()) {
    Serial.println("Failed to find INA219 LOAD chip");
    //while (1) { delay(10); }
     ina_load_status = false;
  } else {
    Serial.println("INA219 LOAD chip found");
     ina_load_status = true;
  }
  // To use a slightly lower 32V, 1A range (higher precision on amps):
  //ina219.setCalibration_32V_1A();
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();

  Serial.println("Measuring voltage and current with INA219 ...");
  
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(load1, OUTPUT);
  pinMode(load2, OUTPUT);
  pinMode(load3, OUTPUT);
  
  //pinMode(pv, OUTPUT);

  pinMode(rs,INPUT);
}

// the loop function runs over and over again forever
void loop() {

  rState = digitalRead(rs);
  //Serial.println(String(rState));
  
  //initialize INA variables
  float shuntvoltage_PV = 0;
  float busvoltage_PV = 0;
  float current_mA_PV = 0;
  float loadvoltage_PV = 0;
  float power_mW_PV = 0;

  float shuntvoltage_LOAD = 0;
  float busvoltage_LOAD = 0;
  float current_mA_LOAD = 0;
  float loadvoltage_LOAD = 0;
  float power_mW_LOAD = 0;

  //read INA values
  shuntvoltage_PV = ina219_PV.getShuntVoltage_mV();
  //this is the total voltage of the circuit under test (measured between Vin- and GND.
  busvoltage_PV = ina219_PV.getBusVoltage_V();
  current_mA_PV = ina219_PV.getCurrent_mA();
  power_mW_PV = ina219_PV.getPower_mW();
  loadvoltage_PV = busvoltage_PV + (shuntvoltage_PV / 1000);

  shuntvoltage_LOAD = ina219_LOAD.getShuntVoltage_mV();
  //this is the total voltage of the circuit under test (measured between Vin- and GND.
  busvoltage_LOAD = ina219_LOAD.getBusVoltage_V();
  current_mA_LOAD = ina219_LOAD.getCurrent_mA();
  power_mW_LOAD = ina219_LOAD.getPower_mW();
  loadvoltage_LOAD = busvoltage_LOAD + (shuntvoltage_LOAD / 1000);

  //print system data
  Serial.println("*** SYSTEM DATA ***");
  if(rState==0){
      Serial.println("Modules: " + String(rState + 1));
  } else {
      Serial.println("Modules: " + String(rState + 1));
  }
  Serial.println("");

  //print INA readings
  Serial.println("*** PV DATA ***");
  //Serial.print("Bus Voltage:   "); Serial.print(busvoltage_PV); Serial.println(" V");
  //Serial.print("Shunt Voltage: "); Serial.print(shuntvoltage_PV); Serial.println(" mV");
  Serial.print("Load Voltage:  "); Serial.print(loadvoltage_PV); Serial.println(" V");
  Serial.print("Current:       "); Serial.print(current_mA_PV); Serial.println(" mA");
  Serial.print("Power:         "); Serial.print(power_mW_PV); Serial.println(" mW");
  Serial.println("");

    Serial.println("*** LOAD DATA ***");
    //Serial.print("Bus Voltage:   "); Serial.print(busvoltage_LOAD); Serial.println(" V");
    //Serial.print("Shunt Voltage: "); Serial.print(shuntvoltage_LOAD); Serial.println(" mV");
    Serial.print("Load Voltage:  "); Serial.print(loadvoltage_LOAD); Serial.println(" V");
    Serial.print("Current:       "); Serial.print(current_mA_LOAD); Serial.println(" mA");
    Serial.print("Power:         "); Serial.print(power_mW_LOAD); Serial.println(" mW");
    Serial.println("");

  if(power_mW_PV <= 0.0){
    digitalWrite(load1, LOW);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(load2, LOW);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(load3, LOW);   // turn the LED on (HIGH is the voltage level)
  } else {
    if(power_mW_PV > 0.0){
      digitalWrite(load1, HIGH);   // turn the LED on (HIGH is the voltage level)
    }
  
    if(power_mW_PV > 10.0){
      digitalWrite(load2, HIGH);   // turn the LED on (HIGH is the voltage level)
    }
  
    if(power_mW_PV > 30.0){
      digitalWrite(load3, HIGH);   // turn the LED on (HIGH is the voltage level)
    }
  }
  delay(3000);                       // wait for 3 seconds
  
}
