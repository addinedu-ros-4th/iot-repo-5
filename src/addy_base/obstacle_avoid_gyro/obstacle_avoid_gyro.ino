#include <Wire.h>
#include "./Addy_SmartMobility.h"
#include <SoftwareSerial.h>

Addy_SmartMobility amr = Addy_SmartMobility();
// SoftwareSerial BTSerial(4, 5);

const int trigPinFront = 2;  // 앞
const int echoPinFront = 3;

const int trigPinRight = 4;  // 우
const int echoPinRight = 5;

const int trigPinBack = 6;  // 뒤
const int echoPinBack = 7;

const int trigPinLeft = 8;  // 좌
const int echoPinLeft = 9;

static float angle[3]={0,}, vec;
int speed = 160;
// 회피할 거리 (센티미터)
const int avoidanceDistance = 10;

void setup() {
  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT);
  pinMode(trigPinBack, OUTPUT);
  pinMode(echoPinBack, INPUT);
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);

  if (!amr.begin()) {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1)
      ;
  }
  Serial.begin(9600);
  amr.setSpeed(200);

  // Wire init
  Wire.begin();
  // Power Management
  Wire.beginTransmission(0x68);
  Wire.write(107);
  Wire.write(0);
  Wire.endTransmission();
  // Register 26
  for(uint8_t i = 2; i <= 7; i++)
  {
    Wire.beginTransmission(0x68);
    Wire.write(26);
    Wire.write(i << 3 | 0x03);
    Wire.endTransmission();
  }
  // Register 27
  Wire.beginTransmission(0x68);
  Wire.write(27);
  Wire.write(3 << 3);
  Wire.endTransmission();
  // Register 28
  Wire.beginTransmission(0x68);
  Wire.write(28);
  Wire.write(0);
  Wire.endTransmission();

}


float getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;

  return distance;
}
int16_t offset[3] = {32, 15, -12};

int get_Z() {
  uint8_t i;
  static int16_t acc_raw[3]={0,}, gyro_raw[3]={0,};
  // Get Accel
  Wire.beginTransmission(0x68);
  Wire.write(59);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 6);
  for(i = 0; i < 3; i++) acc_raw[i] = (Wire.read() << 8) | Wire.read();
  // Get Gyro
  Wire.beginTransmission(0x68);
  Wire.write(67);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 6);
  for(i = 0; i < 3; i++)
    gyro_raw[i] = gyro_raw[i] * 0.8 + 0.2 * (((Wire.read() << 8) | Wire.read()) - offset[i]);
  // Get DT
  static unsigned long p = 0;
  unsigned long c = micros();
  float dt = (c - p) * 0.000001F;
  p = c;
  // Gyro Rate
  float gyro_rate[3];
  for(i = 0; i < 3; i++) gyro_rate[i] = gyro_raw[i] / 16.4 * dt;
  // Calculate
  vec = sqrt(pow(acc_raw[0], 2) + pow(acc_raw[2], 2));
  angle[0] = (angle[0] + gyro_rate[0]) * 0.98
    + atan2(acc_raw[1], vec) * RAD_TO_DEG * 0.02;
  vec = sqrt(pow(acc_raw[1], 2) + pow(acc_raw[2], 2));
  angle[1] = (angle[1] - gyro_rate[1]) * 0.98
    + atan2(acc_raw[0], vec) * RAD_TO_DEG * 0.02;
  // Serial print
  angle[2] += gyro_rate[2];
  char str[50], a1[10], a2[10], a3[10];
  dtostrf(angle[0], 4, 3, a1);
  dtostrf(angle[1], 4, 3, a2);
  dtostrf(angle[2], 4, 3, a3);

  return atoi(a1);

}
void resetAngle() {
  Serial.println("Resetting Angle!");
  for (int i = 0; i < 3; i++) {
    angle[i] = 0;
  }
}

void correction_F() {
  int z_ang = get_Z();

  int delta = 10;
  
  if (z_ang > 3){
    amr.setSpeed(2, speed + delta);
    amr.setSpeed(3, speed - delta);
  }
  else if(z_ang < -3) {
    amr.setSpeed(2, speed - delta);
    amr.setSpeed(3, speed + delta);
  }
  else {
    amr.setSpeed(2, speed);
    amr.setSpeed(3, speed);
  }
}

void correction_S() {
  int z_ang = get_Z();

  int delta = 10;
  
  if (z_ang > 3){
    amr.setSpeed(4, speed + delta);
    amr.setSpeed(1, speed - delta);
  }
  else if(z_ang < -3) {
    amr.setSpeed(4, speed - delta);
    amr.setSpeed(1, speed + delta);
  }
  else {
    amr.setSpeed(4, speed);
    amr.setSpeed(1, speed);
  }
}

void loop() {
  float distanceFront = getDistance(trigPinFront, echoPinFront);
  float distanceBack = getDistance(trigPinBack, echoPinBack);
  float distanceLeft = getDistance(trigPinLeft, echoPinLeft);
  float distanceRight = getDistance(trigPinRight, echoPinRight);

  enum AvoidanceState {
    NO_OBSTACLE,
    AVOIDING_BACK,
    AVOIDING_FRONT,
    AVOIDING_LEFT,
    AVOIDING_RIGHT,
    STOPPED
  };

  AvoidanceState avoidanceState = NO_OBSTACLE;

  switch (avoidanceState) {
    case NO_OBSTACLE:
      // 장애물이 있는지 확인
      if (distanceFront <= avoidanceDistance) {
        avoidanceState = AVOIDING_BACK;
      } else if (distanceBack <= avoidanceDistance) {
        avoidanceState = AVOIDING_FRONT;
      } else if (distanceRight <= avoidanceDistance) {
        avoidanceState = AVOIDING_LEFT;
      } else if (distanceLeft <= avoidanceDistance) {
        avoidanceState = AVOIDING_RIGHT;
      } else {
        correction_F();
        amr.moveF(200);
      }

    case AVOIDING_BACK:
      if (distanceFront < avoidanceDistance) {
        amr.stopAll();

        if (distanceRight > distanceLeft && distanceRight > avoidanceDistance) {
          amr.rotate(1, 600); // CW
          resetAngle();
          break;
        }
        else if (distanceLeft > distanceRight && distanceLeft > avoidanceDistance){
          amr.rotate(2, 600); // CCW
          resetAngle();
          break;
        }
        else {
          amr.moveB(300);
          break;
        }
        break;
      }

    case AVOIDING_FRONT:
      if (distanceBack < avoidanceDistance) {
        correction_F();
        amr.moveF(300);
        // break;
      }

    case AVOIDING_LEFT:
      if (distanceRight < avoidanceDistance) {
        correction_S();
        amr.moveL(300);
        // break;
      }

    case AVOIDING_RIGHT:
      if (distanceLeft < avoidanceDistance) {
        correction_S();
        amr.moveR(300);
        // break;
      }
  }

  Serial.print("Front: ");
  Serial.print(distanceFront);
  Serial.print(" cm   Back: ");
  Serial.print(distanceBack);
  Serial.print(" cm   Left: ");
  Serial.print(distanceLeft);
  Serial.print(" cm   Right: ");
  Serial.print(distanceRight);
  Serial.println(" cm");
}


