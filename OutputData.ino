#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);


//Define FSR Sensors and the ports 
#define numFSR 3 //define number of FSRs 
#define FSR1 A1 //Pin connected to FSR1
#define FSR2 A2 //Pin connected to FSR2 
#define FSR3 A3 //Pin connected to FSR3 
#define FSR4 A4 //Pin connected to FSR4

//define variables to store sensor readings 
int FSR1Val; 
int FSR2Val;
int FSR3Val; 
int FSR4Val;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  //Initialize sensor 
  if (!accel.begin()) {
    Serial.println("No ADXL detected!!");
  }
  else {
    accel.setRange(ADXL345_RANGE_16_G);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  FSR1Val = analogRead(FSR1);
  FSR2Val = analogRead(FSR2);
  FSR3Val = analogRead(FSR3);
  FSR4Val = analogRead(FSR4);
  sensors_event_t event;
  accel.getEvent(&event);
  //display results, one line for FSR results, one line for accel results
  Serial.print(","); Serial.print(FSR1Val);
  Serial.print(","); Serial.print(FSR2Val);
  Serial.print(","); Serial.print(FSR3Val);
  Serial.print(","); Serial.print(event.acceleration.x); 
  Serial.print(","); Serial.print(event.acceleration.y); 
  Serial.print(","); Serial.print(event.acceleration.z); 
  Serial.print(","); Serial.print(FSR4Val); Serial.println(",");
  /*Serial.print(" FSR2: ");
  Serial.print(FSR2Val);
  Serial.print(" FSR3: ");
  Serial.println(FSR3Val);*/
  delay(250);
}
