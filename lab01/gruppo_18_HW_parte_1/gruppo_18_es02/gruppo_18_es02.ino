#include <TimerOne.h>

const int RLED_PIN = 11;
const int GLED_PIN = 12;

const float RLED_HALFPERIOD = 1.5;
const float GLED_HALFPERIOD = 3.5;

int redLedStatus = LOW;
int greenLedStatus = LOW;

void serialPrintStatus() {
  if(Serial.available() >0) {
    volatile int inByte = Serial.read();
    if(inByte == 'R') {
        Serial.print("LED R: Status ");
        Serial.println(redLedStatus, BIN);
        return;
    }
    if(inByte == 'G') {
        noInterrupts();
       Serial.print("LED G: Status ");
       Serial.println(greenLedStatus, BIN);
       interrupts();
       return;
      }
     Serial.println("Invalid command");
  }
}

void blinkGreen() {
    greenLedStatus = !greenLedStatus;
    digitalWrite(GLED_PIN, greenLedStatus);
}

void blinkRed() {
    redLedStatus = !redLedStatus;
    digitalWrite(RLED_PIN, redLedStatus);
    delay(RLED_HALFPERIOD *1e03);
}

void setup() {
  pinMode(RLED_PIN, OUTPUT);
  pinMode(GLED_PIN, OUTPUT);
  Timer1.initialize(GLED_HALFPERIOD * 1e06);
  Timer1.attachInterrupt(blinkGreen);
  Serial.begin(9600);
  while(!Serial);
  Serial.println("lab1.2 starting...");
}

// the loop function runs over and over again forever
void loop() {
  blinkRed();
  serialPrintStatus();
}
