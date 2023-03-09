#include <TimerOne.h>
#include <String.h>
#include <math.h>
#include <limits.h>
#include <LiquidCrystal_PCF8574.h>
#define TEMPERATURE_CONTROL_COMMANDS 8

typedef enum { temperature_status, presence_status, conditioning_status, min_conditioning_temperature, max_conditioning_temperature } pages; //different types of lcd pages
typedef enum { absent, present, timeout_p, timeout_n } mode;   //different modes of detecting/not detecting presence
const String hashTable[8] = { "PFTM", "PHTM", "PFTm", "PHTm", "AFTM", "AHTM", "AFTm", "AHTm" };   //hash table to easily make user change set-point temperatures

//pwm piloting values
const int MIN_CONDITIONING_VALUE = 0;
const int MAX_CONDITIONING_VALUE = 255;

//set-points fan temperatures: [absent mode temperature, presence mode temperature]
volatile int MIN_FAN_TEMPERATURE[2] = { 28, 24 };
volatile int MAX_FAN_TEMPERATURE[2] = { 32, 36 };

//set-points heater temperatures: [absent mode temperature, presence mode temperature]
volatile int MIN_HEATER_TEMPERATURE[2] = { 14, 12 };
volatile int MAX_HEATER_TEMPERATURE[2] = { 22, 24 };

const int TEMP_PIN = A0;
const int B = 4275;
const long int R0 = 100000;
const int Vcc = 1023;

const int HEATER_PIN = 11;  //pwm pin
const int FAN_PIN = 6;  //pwm pin
const int PIR_PIN = 12;
const int PIR_LEDPIN = 8;
const int NS_PIN = 7; //interrupt pin
     
volatile mode presence_mode;      //records the current detecting-presence status for both pir & ns (absence mode, presence mode, timeout mode)
volatile int presenceled_status;  //set presence led status { ON: presence detected, OFF: no presence detected, BLINKING: pir sensor or noise sensor in timeout mode}
volatile int tot_count;           //records the total people counted by noise sensor and pir sensor

const unsigned long timeout_pir = 600 * 1e03;           //pir timeout: 10 min
const unsigned long timeout_ns = 300 * 1e03;            //noise sensor timeout: 5 min
const unsigned long blinkingled_period = 0.5 * 1e06;          //presence led blinkin semiperiod (microseconds) in timeout mode
volatile unsigned long startTime_pir;                   //stores the initial time to evaluate the elapsed time for pir sensor
volatile unsigned long startTime_ns;                    //stores the initial time to evaluate the elapsed time for noise sensor
volatile unsigned long startTime_clap;                  //stores the initial time to evaluate the elapsed time for detecting a second clap
volatile unsigned int sound_events_count;               //records the sound events registered by the noise sensor to detect presence
const unsigned int sound_events = 10;                    //number of sound events to record by the noise sensor to confirm a presence 
volatile unsigned long startTime_sound;                 //stores the initial time to evaluate the elapsed time to confirm a presence by the noise sensor
const unsigned long sound_events_interval = 20 * 1e03;  //detecting sound_events interval to confirm presence
volatile unsigned long clap_interval; 
volatile unsigned int clap_count;

LiquidCrystal_PCF8574 lcd(0x27);
volatile pages lcd_page;

//'grade' char with creation specs as mentioned in LiquidCrystal_PCF8574.h docs
byte grade[8] = {
  0b00111,
  0b00101,
  0b00111,
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};

//returns 0 if absent, 1 if present
int isPresent(mode presence_mode) {
  if(presence_mode > 0) return 1;     //supposing that timeout modes means someone still present
  return 0;
}

//returns a float value between 0 and 1 for the conditioning fan motor
float getFanValue(float surroundingTemperature, mode presence_mode) {
  volatile int presence = isPresent(presence_mode);
  if(surroundingTemperature >= MIN_FAN_TEMPERATURE[presence] && surroundingTemperature <= MAX_FAN_TEMPERATURE[presence])
    return (float)(surroundingTemperature - MIN_FAN_TEMPERATURE[presence])/(MAX_FAN_TEMPERATURE[presence] - MIN_FAN_TEMPERATURE[presence]);
  if(surroundingTemperature > MAX_FAN_TEMPERATURE[presence])
    return 1.0;
  return 0.0;
}

//returns a float value between 0 and 1 for the heater
float getHeaterValue(float surroundingTemperature, mode presence_mode) {
  volatile int presence = isPresent(presence_mode);
  if(surroundingTemperature >= MIN_HEATER_TEMPERATURE[presence] && surroundingTemperature <= MAX_HEATER_TEMPERATURE[presence])
    return (float)(1.0 - (surroundingTemperature - MIN_HEATER_TEMPERATURE[presence])/(MAX_HEATER_TEMPERATURE[presence] - MIN_HEATER_TEMPERATURE[presence]));
  if(surroundingTemperature < MIN_HEATER_TEMPERATURE[presence])
    return 1.0;
  return 0.0;
}

//function to put sensors in timeout mode: waiting to dectect any other presence
void startTimeout(mode sensor) {
  if(sensor == timeout_p) {
    presence_mode = timeout_p; 
    startTime_pir = millis();
  }
  if(sensor == timeout_n) {
    presence_mode = timeout_n;
    startTime_ns = millis();
  }
  Timer1.restart();   //presence led starts blinking
}

//function to confirm a presence detected
void confirmPresence() {
  tot_count++;
  presence_mode = present;
  Timer1.stop();  //stops the presence led from blinking
  digitalWrite(PIR_LEDPIN, present); //set led always-on
  sound_events_count = 0;
}

//function for pir sensor
void checkPresencePir() {
  int pir_status = digitalRead(PIR_PIN);
  if(pir_status == HIGH)
    if(presence_mode == absent || presence_mode == timeout_p || presence_mode == timeout_n)
      confirmPresence();
  else {
    if(presence_mode == present) 
      startTimeout(timeout_p);
    if(presence_mode == timeout_p && timeoutExpired(millis(), startTime_pir, timeout_pir))
      absentMode();
  }
}


//interrupt function for noise sensor
void checkPresenceNS() {
  sound_events_count++;
}

//time-based function for presence_mode: if no presence detected by pir or noise sensor after timeouts' end --> absent mode
void absentMode() { 
  Timer1.stop();  //stops the presence led from blinking
  presence_mode = absent;  
  digitalWrite(PIR_LEDPIN, absent);
}

//time-based interrupt to make led blink
void blinkingLed() {
  presenceled_status = !presenceled_status;
  digitalWrite(PIR_LEDPIN, presenceled_status);
}

//function to print the 'grade' character on the lcd
void printGrade(int col, int row) {
  lcd.setCursor(col,row);
  lcd.write((byte)0);
  lcd.print("C");
}

//function to make lcd switch from different pages to display information every 2 seconds (delay() in loop())
void lcdDisplayPage(pages lcd_page, float temperature, mode presence_mode, float fan_percentage, float heater_percentage, int count) {
  volatile int presence = isPresent(presence_mode);
  switch(lcd_page) {
    case temperature_status: 
      lcd.clear();
      lcd.print("  Temperature:");
      lcd.setCursor(4,1);
      lcd.print(temperature);
      printGrade(9,1);
      break;
    case presence_status:
      lcd.clear();
      lcd.print(" Presence: ");
      (presence > 0) ? lcd.print("D") : lcd.print("N/D");
      lcd.setCursor(0,1);
      lcd.print(" Total count: ");
      lcd.print(count);
      break;
    case conditioning_status:
      lcd.clear();
      lcd.print("   Fan: ");
      lcd.print(fan_percentage);
      lcd.print("%");
      lcd.setCursor(0,1);
      lcd.print("  Heat: ");
      lcd.print(heater_percentage);
      lcd.print("%");
      break;
    case min_conditioning_temperature:
      lcd.clear();
      lcd.print(" Fan(min): ");
      lcd.print(MIN_FAN_TEMPERATURE[presence]);
      printGrade(13,0);
      lcd.setCursor(0,1);
      lcd.print("Heat(min): ");
      lcd.print(MIN_HEATER_TEMPERATURE[presence]);
      printGrade(13,1);
      break;
    case max_conditioning_temperature:
      lcd.clear();
      lcd.print(" Fan(max): ");
      lcd.print(MAX_FAN_TEMPERATURE[presence]);
      printGrade(13,0);
      lcd.setCursor(0,1);
      lcd.print("Heat(max): ");
      lcd.print(MAX_HEATER_TEMPERATURE[presence]);
      printGrade(13,1);
      break;
  }
}

//search for integer key from string in the hash table 
int getKey(String temperature) {
    for(int i=0; i<TEMPERATURE_CONTROL_COMMANDS; i++)
      if(temperature.equals(hashTable[i]))
          return i;
    return -1;
}

//function to wait user updating set-point temperatures
void updateInterrupt() {
  lcd.print("Updating");
  lcd.setCursor(0,1);
  lcd.print("temperatures...");
}

//function to display a temperatures control panel in serial terminal
void temperaturesControlPanel() {
  String string, inByte; volatile int key;
  Serial.println();
  Serial.println("TEMPERATURE CONTROL PANEL");
  Serial.println("Type the temperature abbrevation to modify the value...");
  
  Serial.println("\t- PFTM: Presence Fan Temperature Max");
  Serial.println("\t- PHTM: Presence Heat Temperature Max");
  Serial.println("\t- PFTm: Presence Fan Temperature min");
  Serial.println("\t- PHTm: Presence Heat Temperature min");

  Serial.println("\t- AFTM: Absence Fan Temperature Max");
  Serial.println("\t- AHTM: Absence Heat Temperature Max");
  Serial.println("\t- AFTm: Absence Fan Temperature min");
  Serial.println("\t- AHTm: Absence Heat Temperature min");
  Serial.flush();

  lcd.clear();
  updateInterrupt();
  while(Serial.available() == 0);
    string = Serial.readString();
    key = getKey(string);
    if( key < 0 ) {
      Serial.println("Invalid command");
      return;
    }
    Serial.println("Type the new integer value...");
    Serial.flush();
    
    lcd.clear();
    updateInterrupt();
    while(Serial.available() == 0);
    Serial.flush();
    switch(key) {
      case 0: MAX_FAN_TEMPERATURE[1] = Serial.parseInt();
              Serial.print("Presence Fan Temperature Max Updated: ");
              Serial.println(MAX_FAN_TEMPERATURE[1]);
          break;
      case 1: MAX_HEATER_TEMPERATURE[1] = Serial.parseInt();
              Serial.print("Presence Heater Temperature Max Updated: ");
              Serial.println(MAX_HEATER_TEMPERATURE[1]);
          break;
      case 2: MIN_FAN_TEMPERATURE[1] = Serial.parseInt();
              Serial.print("Presence Fan Temperature Min Updated: ");
              Serial.println(MIN_FAN_TEMPERATURE[1]);
          break;
      case 3: MIN_HEATER_TEMPERATURE[1] = Serial.parseInt();
            Serial.print("Presence Heater Temperature Min Updated: ");
            Serial.println(MIN_HEATER_TEMPERATURE[1]);
          break;
      case 4: MAX_FAN_TEMPERATURE[0] = Serial.parseInt();
            Serial.print("Absence Fan Temperature Max Updated: ");
            Serial.println(MAX_FAN_TEMPERATURE[0]);
          break;
      case 5: MAX_HEATER_TEMPERATURE[0] = Serial.parseInt();
            Serial.print("Absence Heater Temperature Max Updated: ");
            Serial.println(MAX_HEATER_TEMPERATURE[0]);
          break;
      case 6: MIN_FAN_TEMPERATURE[0] = Serial.parseInt();
            Serial.print("Absence Fan Temperature Min Updated: ");
            Serial.println(MIN_FAN_TEMPERATURE[0]);
          break;
      case 7: MIN_HEATER_TEMPERATURE[0] = Serial.parseInt();
            Serial.print("Absence Heater Temperature Min Updated: ");
            Serial.println(MIN_HEATER_TEMPERATURE[0]);
          break;
  }
  return;
}

//return 1 if the time interval given is expired, 0 instead
int timeoutExpired(long current, long start, long interval) {
  return ((current - start) >= interval) ? 1 : 0;
}

//function to check presence for the noise sensor at every loop iteration
void presenceNS() {
  volatile int expired_sound = timeoutExpired(millis(), startTime_sound, sound_events_interval);
  volatile int expired_ns = timeoutExpired(millis(), startTime_ns, timeout_ns);
 
  if(sound_events_count > sound_events && !expired_sound) //presence confirmed
    confirmPresence();

  if(expired_sound) {
    sound_events_count = 0;
    startTime_sound = millis();
    if(presence_mode == present)
      startTimeout(timeout_n);
  }

  if(presence_mode == timeout_n && expired_ns) {
    absentMode();
    sound_events_count = 0;
    startTime_sound = millis();
  }
}

//function to detect a double hand-clap
void clapping() {
  int ns_status = digitalRead(NS_PIN);
  if (ns_status == LOW) {
    if (clap_count == 0) {
      startTime_clap = clap_interval = millis();
      clap_count++;
    }
    else if (clap_count > 0 && (millis() - clap_interval) >= 50) {
      clap_interval = millis();
      clap_count++;
    }
  }
  
  if ((millis() - startTime_clap) >= 400) {
    if (clap_count == 2) {
      presenceled_status = !presenceled_status;
      digitalWrite(PIR_LEDPIN, presenceled_status);
    }
    clap_count = 0;
  }
}

void setup() {
  pinMode(HEATER_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(TEMP_PIN, INPUT);
  pinMode(PIR_PIN, INPUT_PULLUP);
  pinMode(PIR_LEDPIN, OUTPUT);
  pinMode(NS_PIN, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(NS_PIN), checkPresenceNS, FALLING);
  Timer1.initialize(blinkingled_period);
  Timer1.attachInterrupt(blinkingLed);
  Timer1.stop();
  
  Serial.begin(9600);
  
  lcd.begin(16,2);
  lcd.setBacklight(255);
  lcd.home();
  lcd.clear();
  lcd.createChar(0, grade);
  lcd_page = temperature_status;

  while(!Serial);
  Serial.println("SMART HOME CONTROLLER");
  Serial.println("\tType 'T' to enter Temperatures Control Panel");

  tot_count = 0;
  presenceled_status = LOW;
  presence_mode = absent;
  sound_events_count = 0;
  digitalWrite(PIR_LEDPIN, presenceled_status);
  startTime_sound = millis();
  startTime_clap = 0;
  clap_interval = 0;
  clap_count = 0;
}


void loop() {

  volatile float a = analogRead(TEMP_PIN);
  volatile float R = (1023.0/a - 1.0) * R0;
  volatile float temp = 1.0/(log(R/R0)/B + 1/298.15) - 273.15; // convert to temperature via datasheet

  checkPresencePir();
  
  noInterrupts();
  presenceNS();
  if(presence_mode == timeout_p && timeoutExpired(millis(), startTime_pir, timeout_pir))
    absentMode();
  interrupts();
  
   //lab02.9: reverse all loop() commentation to try
    //noInterrupts();
    //clapping();
    //interrupts();
  
  volatile float fan_value = getFanValue(temp, presence_mode);
  volatile int fan_percentage = fan_value * 100;
  analogWrite(FAN_PIN, fan_value * MAX_CONDITIONING_VALUE);
  
  volatile float heater_value = getHeaterValue(temp, presence_mode);
  volatile int heater_percentage = heater_value * 100;
  analogWrite(HEATER_PIN, heater_value * MAX_CONDITIONING_VALUE);

  if(lcd_page > max_conditioning_temperature) lcd_page = temperature_status;
  lcdDisplayPage(lcd_page, temp, presence_mode, fan_percentage, heater_percentage, tot_count);
  lcd_page = (pages)(lcd_page + 1);
 
  if(Serial.available() > 0 && Serial.read() == 'T')
    temperaturesControlPanel();
  Serial.flush();
  
 delay(2000);
}
