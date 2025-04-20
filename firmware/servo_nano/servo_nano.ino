#include <Servo.h>

Servo servo;
const int servoPin = 9;
const unsigned long BAUD = 115200;

void setup() {
  Serial.begin(BAUD);
  servo.attach(servoPin);
  servo.write(90);  // center
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    if (line.startsWith("ANGLE:")) {
      int angle = line.substring(6).toInt();
      angle = constrain(angle, 0, 180);
      servo.write(angle);
      Serial.println("OK");
    }
  }
}