#include "Addy_SmartMobility.h"
#include <SoftwareSerial.h>

Addy_SmartMobility sm = Addy_SmartMobility();
SoftwareSerial BTSerial(4, 5);

char data;

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
  if (!sm.begin())
  {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1);
  }
  sm.setSpeed(300);
  sm.moveTo(5);
}

void loop() {
  if (BTSerial.available()) {
    data = BTSerial. read();
    sm.moveTo(data - 48);
  }
}