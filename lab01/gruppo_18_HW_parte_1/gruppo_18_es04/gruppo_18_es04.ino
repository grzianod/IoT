int FAN_PIN = 3;
int current_speed = 0;

void readSerial() {
  if(Serial.available() > 0) {
    volatile int byteIn = Serial.read();
    if(byteIn == '+') {
      if(current_speed > 249) 
        Serial.println("Already at max speed");
        else {
          current_speed += 25;
          analogWrite(FAN_PIN, current_speed);
          Serial.print("Increasing speed: ");
          Serial.println(current_speed);
        }
      return;
    }
    if(byteIn == '-') {
      if(current_speed == 0)
        Serial.println("Already at min speed");
        else {
          current_speed -= 25;
          analogWrite(FAN_PIN, current_speed);
          Serial.print("Decreasing speed: ");
          Serial.println(current_speed);
        }
      return;
    }
    Serial.println("Invalid command");
  }
}

void setup() {
  pinMode(FAN_PIN, OUTPUT);
  analogWrite(FAN_PIN, (int) current_speed);
  Serial.begin(9600);
  while(!Serial);
  Serial.println("lab1.4 starting...");
  Serial.println("Speed: 0");
}

void loop() {
  readSerial();
}
