/*

I intentionally use the const byte construct here
instead of #define. It's less dangerous (no name collision possible)
and safer since variables have scope.
*/
#include <Servo.h>

Servo myservo;
Servo myservo2;
const byte sensor_pin = A0;
const byte CMD_START = 1;

unsigned long previousMillis = 0;        // will store last time we updated

long prev_t = 0;
int sensor_value = 0;
int pos = 0;
byte cmd_id = 0; 

String distance="";
String message = "";

void setup() {
  //Setup input and outputs
  myservo.attach(10);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(9);
  myservo2.write(60);

  Serial.begin(9600);
}

void loop() {

  if(Serial.available() >= 0) {
    cmd_id = Serial.read();
  }
  else{
    cmd_id = 0;
  }
  
  switch(cmd_id){
    case 0:
        myservo.write(50);
      break;
    case CMD_START:
    // start sweeping the servos over the letter
      for (pos = 0; pos <= 50; pos += 1) { // goes from 0 degrees to 50 degrees
        // in steps of 5 degrees
          myservo.write(pos); // tell servo to go to position in variable 'pos'
          delay(15);
          sensor_value = analogRead(sensor_pin);
          distance = int(5748.858*pow(sensor_value, -.868));
          message = String(pos) + "," + String(110) + "," + distance;
          Serial.println(message);
          delay(500);
      }
      message = "";
      break;
    break;
  }
}
