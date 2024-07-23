#include <stdio.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>

#include <string.h>

const int maxAngle = 180;
const int delaySec = 2;

Servo Servo1;
Servo Servo2;
Servo Servo3;
Servo Servo4;
Servo Servo5;
Servo Servo6;
Servo Servo7;
Servo Servo8;
Servo Servo9;
Servo Servo10;
Servo servos[] = {Servo1, Servo2, Servo3, Servo4, Servo5, Servo6, Servo7, Servo8, Servo9, Servo10};

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int DATA[5][10] = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, maxAngle/4, 0, maxAngle/4, 0, 0, maxAngle/4, maxAngle/4, maxAngle/4}, {maxAngle/2, maxAngle/2, maxAngle/2, 0, maxAngle/4, maxAngle/2, maxAngle/2, maxAngle/2, maxAngle/2, maxAngle/4}, {maxAngle/2, maxAngle * 0.75, 180, 0, maxAngle * 0.75, maxAngle * 0.75, maxAngle * 0.75, maxAngle * 0.75, maxAngle * 0.75, maxAngle * 0.75}, {180, 180, 180, 0, 180, 180, 180, 180, 180, 180}};
const String DATES[5] = {"June 14 1990", "June 29 2007", "July 31 2014", "July 24 2023", "August 25 2023"};

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.print("Initializing...");

  for (int i = 1; i <= 10; i++){
    servos[i-1].attach(i);
  }
  
  for (Servo s: servos){
    s.write(0);
  }
} 

int index = 0;
void loop() {
  delay(delaySec * 1000);
  int sIndex = 0;
  for(Servo s : servos){
    s.write(DATA[index][sIndex]);
    sIndex += 1;
  }
  lcd.clear();
  lcd.print(DATES[index]);
  index += 1;
  if (index == 5){
    index = 0;
  }
}