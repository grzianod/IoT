#include <TimerOne.h>

const int RLED_PIN = 11;
const int GLED_PIN = 12;

const float RLED_PERIOD = 1.5;
const float GLED_PERIOD = 3.5;

int redLedStatus = LOW;
int greenLedStatus = LOW;

void blinkGreen() {
    greenLedStatus = !greenLedStatus;
    digitalWrite(GLED_PIN, greenLedStatus);
}

void setup() {
  pinMode(RLED_PIN, OUTPUT);
  pinMode(GLED_PIN, OUTPUT);
  Timer1.initialize(GLED_PERIOD * 1e06);
  Timer1.attachInterrupt(blinkGreen);
}

// the loop function runs over and over again forever
void loop() {
  redLedStatus = !redLedStatus;
  digitalWrite(RLED_PIN, redLedStatus);
  delay(RLED_PERIOD * 1e03);
}
