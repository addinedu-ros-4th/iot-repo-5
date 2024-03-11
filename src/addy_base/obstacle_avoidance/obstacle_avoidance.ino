
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
        amr.moveF(200);
      }

    case AVOIDING_BACK:
      if (distanceFront < avoidanceDistance) {
        amr.stopAll();

        if (distanceRight > distanceLeft && distanceRight > avoidanceDistance) {
          amr.rotate(1, 600); // CW
          break;
        }
        else if (distanceLeft > distanceRight && distanceLeft > avoidanceDistance){
          amr.rotate(2, 600); // CCW
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
        amr.moveF(300);
        // break;
      }

    case AVOIDING_LEFT:
      if (distanceRight < avoidanceDistance) {
        amr.moveL(300);
        // break;
      }

    case AVOIDING_RIGHT:
      if (distanceLeft < avoidanceDistance) {
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


