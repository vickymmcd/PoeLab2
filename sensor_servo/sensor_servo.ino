/*

I intentionally use the const byte construct here
instead of #define. It's less dangerous (no name collision possible)
and safer since variables have scope.
*/
#include <Servo.h>

Servo myservo;
Servo myservo2;
const byte sensor_pin = A0;
const byte CMD_READ_SENSOR = 1;
const byte CMD_MOVE_SERVO1 = 2;
const byte CMD_MOVE_SERVO2 = 3;

unsigned long previousMillis = 0;        // will store last time we updated

long prev_t = 0;
int sensor_value = 0;
int pos = 0;
int pos2 = 0;
byte cmd_id = 0; 

String result="";
String distance="";

void setup() {
  //Setup input and outputs
  myservo.attach(10);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(9);
  Serial.begin(9600);
}

void loop() {
  sensor_value = analogRead(sensor_pin);
  distance = int(5748.858*pow(sensor_value, -.868));

  if(Serial.available() > 0) {
    cmd_id = Serial.read();
  }
  else{
    cmd_id = 0;
  }
  
  switch(cmd_id){
    case CMD_READ_SENSOR:
      result = result + "Sensor reads: " + sensor_value;
      distance = distance + "Distance is: " + distance;
      Serial.println(result);
      Serial.println(distance);
      result = "";
      distance = "";
      break;
    case CMD_MOVE_SERVO1:
      result = result + "Moving the servo now";
      Serial.println(result);
      for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        myservo2.write(pos);
        delay(15);                       // waits 15ms for the servo to reach the position
      }
      for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        myservo2.write(pos);
        delay(15);                       // waits 15ms for the servo to reach the position
      }
      result = "";
      break;
    case CMD_MOVE_SERVO2:
      result = result + "Sweeping the servos now";
      Serial.println(result);
      for (pos = 0; pos <= 50; pos += 5) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
          myservo.write(pos); // tell servo to go to position in variable 'pos'
          delay(15);
        for (pos2=10; pos2<=110; pos2+=1){
            myservo2.write(pos2);
            delay(15);
        }
      }
      result = "";
      break;
    break;
  }
}

// If the full interval has occured, return true
bool waitNoDelay(long millisToWait){
  unsigned long currentMillis = millis();
      if (currentMillis - previousMillis >= millisToWait) {
        // save the last time you blinked the LED
        previousMillis = currentMillis;
        return true;
      }
      else{
        return false;
      }
  }

