#include <math.h>
#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd(0x27);
const int TEMP_PIN = A0;
const int B = 4275;
const long int R0 = 100000;
const int Vcc = 1023;

byte gradi[8] = {
  0b00111,
  0b00101,
  0b00111,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

void setup() {
  pinMode(TEMP_PIN, INPUT);
  lcd.begin(16,2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();
  lcd.print("Temperature:");
  lcd.createChar(0, gradi);
  lcd.setCursor(10,1);
  lcd.write((byte)0);
  lcd.setCursor(11,1);
  lcd.print("C");
}

void loop() {
  volatile float a = analogRead(TEMP_PIN); //<-- valore di tensione del pin
  volatile float R = 1023.0/a-1.0;
   R = R0*R;
  volatile float temp = 1.0/(log(R/R0)/B + 1/298.15)-273.15; // convert to temperature via datasheet
  lcd.setCursor(4,1);  //invio esclusivo variazione di temperatura sul bus I2C
  lcd.print(temp);
  delay(500);
}
