/*

I intentionally use the const byte construct here
instead of #define. It's less dangerous (no name collision possible)
and safer since variables have scope.
*/
const byte PUSH_BUTTON = 8;
const byte sensor_pin = A0;
const byte CMD_READ_SENSOR = 1;
const byte CMD_READ_BTN = 2;

long prev_t = 0;
int sensor_value = 0;
byte cmd_id = 0; 

byte btn_state = LOW;

String result="";
String distance="";

void setup() {
  //Setup input and outputs: LEDs out, pushbutton in.
  pinMode(PUSH_BUTTON, INPUT);
  Serial.begin(9600);
}

void loop() {
  byte btn_state = digitalRead(PUSH_BUTTON);
  sensor_value = analogRead(sensor_pin);
  distance = int(5748.858*pow(sensor_value, -.868));

  if(Serial.available() > 0) {
    cmd_id = Serial.read();
  } else {
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
    case CMD_READ_BTN:
      result = result + "Button state: " + btn_state;
      Serial.println(result);
      result = "";
      break;
    break;
  }
}

