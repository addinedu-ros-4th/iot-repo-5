#include <Kocoafab_SmartMobility.h>
Kocoafab_SmartMobility sm = Kocoafab_SmartMobility();

int sensitivity = 50;

void setup() 
{
  Serial.begin(9600);
  if (!sm.begin()) {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1);
  } 
sm.setSpeed(100);
sm.moveTo(5);
}

void loop() {
  if (analogRead(A0) > sensitivity && analogRead(A1) > sensitivity) {
    sm.moveTo(8);
  }
  else if (analogRead(A0) > sensitivity && analogRead(A1) < sensitivity) {
    sm.rotate(CCW);
  }
  else if (analogRead(A0) < sensitivity && analogRead(A1) > sensitivity) {
    sm.rotate(CW);
  }
  else if (analogRead(A0) < sensitivity && analogRead(A1) < sensitivity) {
    sm.moveTo(2);
  }
  delay(10);
}