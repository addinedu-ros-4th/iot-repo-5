#include "./Addy_SmartMobility.h"
#include <SoftwareSerial.h>

Addy_SmartMobility sm = Addy_SmartMobility();
SoftwareSerial BTSerial(4, 5);

char data;
int speed = 0;
int delta = 0;

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
  if (!sm.begin()) {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1)
      ;
  }

  speed = 125;
  sm.setSpeed(speed);
  sm.moveTo(5);
}

void correction(int cmd) {
  if (cmd == -38) {
    return;
  }

  if (cmd == 2 || cmd == 8) {
    delta = 20;
    sm.setSpeed(3, speed + delta);
  } else if (cmd == 4) {
    delta = 4;
    sm.setSpeed(4, speed + delta);
  } else if (cmd == 6) {
    delta = 4;
    sm.setSpeed(1, speed + delta);
  }
  else {
    delta = 0;
    sm.setSpeed(speed);
  }
}

void loop() {
  if (BTSerial.available()) {
    data = BTSerial.read();
    int cmd = data - 48;

    correction(cmd);

    sm.moveTo(cmd);
  }
}