#include <Wire.h>
const int RLED_PIN = 11;
const int PIR_PIN = 7;

volatile int tot_count = 0;

void checkPresence() {
  volatile int pirStatus = digitalRead(PIR_PIN);
  Serial.print(pirStatus);
  digitalWrite(RLED_PIN, pirStatus);
  if(pirStatus == HIGH) tot_count++;
}

void setup()
{
  pinMode(PIR_PIN, INPUT_PULLUP);
  pinMode(RLED_PIN, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(PIR_PIN), checkPresence, CHANGE);
  
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Lab 1.3 starting...");
}

void serialPrintStatus() {
    noInterrupts();
    Serial.print("Total people count: ");
    Serial.println(tot_count);
    interrupts();
}
  
void loop()
{
      serialPrintStatus();
      delay(3*1e03);
}
