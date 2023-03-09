#include <math.h>
const int TEMP_PIN = A0;
const int B = 4275;
const long int R0 = 100000;
const int Vcc = 1023;

void setup() {
  pinMode(TEMP_PIN, INPUT);
  Serial.begin(9600);
  while(!Serial);
  Serial.println("lab1.5 starting...");
}

void loop() {
  volatile float a = analogRead(TEMP_PIN);
  volatile float R = ((Vcc/a)-1)*R0;
  volatile float temp = (1.0/((log(R/R0)/B)+(1/298.15))) - 273.15;
  Serial.print("Temperature: ");
  Serial.println(temp);
  delay(1000);
}
