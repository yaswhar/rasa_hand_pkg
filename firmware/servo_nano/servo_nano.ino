#include <Servo.h>

Servo servo;
const int servoPin = 9;
const unsigned long BAUD = 115200;

void setup() {
  Serial.begin(BAUD);
  Serial.setTimeout(10);      // don’t block too long
  servo.attach(servoPin);
  servo.write(90);            // start centered
}

void loop() {
  if (Serial.available() > 0) {
    // Expect exactly “ANGLE:<number>\n”
    // parseInt skips non‑digits until it finds digits
    int angle = Serial.parseInt(); 
    angle = constrain(angle, 0, 180);
    servo.write(angle);
    Serial.println("OK");
    // consume the trailing newline if it’s there
    if (Serial.peek() == '\n') Serial.read();
  }
}