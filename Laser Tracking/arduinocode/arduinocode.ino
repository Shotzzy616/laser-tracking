#include <Servo.h>

Servo servoX;
Servo servoY;
int laser = 12;

void setup() {
  Serial.begin(2000000);
  servoX.attach(9);
  servoY.attach(10);
  pinMode(laser, OUTPUT);

}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    int commaIndex = data.indexOf(',');
    if (commaIndex != -1) {
      int servoXPos = data.substring(0, commaIndex).toInt();
      int servoYPos = data.substring(commaIndex + 1).toInt();
      int servoXAngle = map(servoXPos, 0, 700, 0, 180);
      int servoYAngle = map(servoYPos, 0, 600, 0, 180);

      Serial.print("Servo X Angle: ");
      Serial.print(servoXAngle);
      Serial.print("  Servo Y Angle: ");
      Serial.println(servoYAngle);

      servoX.write(servoXAngle);
      servoY.write(servoYAngle);
      digitalWrite(laser, HIGH);
    }
  }
}
