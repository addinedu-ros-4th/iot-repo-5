#include "ESP8266.h"
#include <Wire.h>
#include <SoftwareSerial.h>

#include "./Addy_SmartMobility.h"


#define SSID "AIE_509_2.4G"
#define PASSWORD "addinedu_class1"
#define HOST_NAME "192.168.0.23"
#define HOST_PORT (9090)

enum AvoidanceState {
  NO_OBSTACLE,
  AVOIDING_BACK,
  AVOIDING_FRONT,
  AVOIDING_LEFT,
  AVOIDING_RIGHT,
  STOPPED
};
AvoidanceState avoidanceState = NO_OBSTACLE;

SoftwareSerial mySerial(12, 13); /* RX:13, TX:12 */
ESP8266 wifi(mySerial);

bool tcp_status = false;
Addy_SmartMobility addy = Addy_SmartMobility();

char data;
int speed = 0;
int delta = 0;
int cmd = 0;

const int trigPinFront = 2;  // 앞
const int echoPinFront = 3;
const int trigPinRight = 4;  // 우
const int echoPinRight = 5;
const int trigPinBack = 6;  // 뒤
const int echoPinBack = 7;
const int trigPinLeft = 8;  // 좌
const int echoPinLeft = 9;

static float angle[3] = {
  0,
},
             vec;
// 회피할 거리 (센티미터)
const int avoidanceDistance = 20;

void setup() {
  Serial.begin(9600);
  connect_wifi();

  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT);
  pinMode(trigPinBack, OUTPUT);
  pinMode(echoPinBack, INPUT);
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);

  if (!addy.begin()) {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1)
      ;
  }
  imu_i2c_init();

  speed = 125;
  addy.setSpeed(speed);
  addy.moveTo(5);
}


void loop() {

  uint8_t buffer[256] = { 0 };
  int z_val = get_Z();
  int test = 12345;

  char char_z_val[10];
  char char_test[10];

  sprintf(char_z_val, "%d", z_val);
  sprintf(char_test, "%d", test);

  char merge_data[100];
  sprintf(merge_data, "%s,%s", char_z_val, char_test);

  tcp_on();
  if (tcp_status) {
    // char *hello = "Hello, this is client!";
    // wifi.send((const uint8_t *)hello, strlen(hello));
    // wifi.send((const uint8_t *)&char_z_val, strlen(char_z_val));
    // wifi.send((const uint8_t *)&char_test, strlen(char_test));
    wifi.send((const uint8_t *)&merge_data, strlen(merge_data));


    uint32_t len = wifi.recv(buffer, sizeof(buffer), 10000);
    if (len > 0) {
      Serial.print("Received:[");
      for (uint32_t i = 0; i < len; i++) {
        Serial.print((char)buffer[i]);
      }
      Serial.print("]\r\n");
      cmd = (int)buffer[0] - 48;
      Serial.println(cmd);
    }
  }
  tcp_off();

  Serial.print("IMU : ");
  Serial.println(z_val);

  if (cmd == 2 || cmd == 8) {
    correction_F(z_val);
  } else if (cmd == 4 || cmd == 6) {
    correction_S(z_val);
  }

  addy.moveTo(cmd);

}

void tcp_on() {
  if (wifi.createTCP(HOST_NAME, HOST_PORT)) {
    // Serial.print("create tcp ok\r\n");
    tcp_status = true;
  } else {
    // Serial.print("create tcp err\r\n");
    tcp_status = false;
  }
}

void tcp_off() {
  if (wifi.releaseTCP()) {
    // Serial.print("release tcp ok\r\n");
    tcp_status = false;
  } else {
    // Serial.print("release tcp err\r\n");
    tcp_status = true;
  }
}

void connect_wifi() {
  Serial.print("FW Version:");
  Serial.println(wifi.getVersion().c_str());

  if (wifi.setOprToStationSoftAP()) {
    Serial.print("to station + softap ok\r\n");
  } else {
    Serial.print("to station + softap err\r\n");
  }

  if (wifi.joinAP(SSID, PASSWORD)) {
    Serial.print("Join AP success\r\n");
    Serial.print("IP:");
    Serial.println(wifi.getLocalIP().c_str());
  } else {
    Serial.print("Join AP failure\r\n");
  }

  if (wifi.disableMUX()) {
    Serial.print("single ok\r\n");
  } else {
    Serial.print("single err\r\n");
  }

  Serial.print("setup end\r\n");
}


void bluetooth_test() {
  // if (BTSerial.available()) {
  //   data = BTSerial.read();
  //   cmd = data - 48;
  //   correction(cmd);
  //   addy.moveTo(cmd);
  // }
}

void correction(int cmd) {
  if (cmd == -38) {
    return;
  }
  if (cmd == 2 || cmd == 8) {
    delta = 20;
    addy.setSpeed(3, speed + delta);
  } else if (cmd == 4) {
    delta = 4;
    addy.setSpeed(4, speed + delta);
  } else if (cmd == 6) {
    delta = 4;
    addy.setSpeed(1, speed + delta);
  } else {
    delta = 0;
    addy.setSpeed(speed);
  }
}

void imu_i2c_init() {
  // Wire init
  Wire.begin();
  // Power Management
  Wire.beginTransmission(0x68);
  Wire.write(107);
  Wire.write(0);
  Wire.endTransmission();
  // Register 26
  for (uint8_t i = 2; i <= 7; i++) {
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
int16_t offset[3] = { 32, 15, -12 };

int get_Z() {
  uint8_t i;
  static int16_t acc_raw[3] = {
    0,
  },
                 gyro_raw[3] = {
                   0,
                 };
  // Get Accel
  Wire.beginTransmission(0x68);
  Wire.write(59);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 6);
  for (i = 0; i < 3; i++) acc_raw[i] = (Wire.read() << 8) | Wire.read();
  // Get Gyro
  Wire.beginTransmission(0x68);
  Wire.write(67);
  Wire.endTransmission();
  Wire.requestFrom(0x68, 6);
  for (i = 0; i < 3; i++)
    gyro_raw[i] = gyro_raw[i] * 0.8 + 0.2 * (((Wire.read() << 8) | Wire.read()) - offset[i]);
  // Get DT
  static unsigned long p = 0;
  unsigned long c = micros();
  float dt = (c - p) * 0.000001F;
  p = c;
  // Gyro Rate
  float gyro_rate[3];
  for (i = 0; i < 3; i++) gyro_rate[i] = gyro_raw[i] / 16.4 * dt;
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

  return atoi(a3);
}

void resetAngle() {
  Serial.println("Resetting Angle!");
  for (int i = 0; i < 3; i++) {
    angle[i] = 0;
  }
}

void correction_F(int z_ang) {
  int delta = 10;

  if (z_ang > 3) {
    addy.setSpeed(2, speed + delta);
    addy.setSpeed(3, speed - delta);
  } else if (z_ang < -3) {
    addy.setSpeed(2, speed - delta);
    addy.setSpeed(3, speed + delta);
  } else {
    addy.setSpeed(2, speed);
    addy.setSpeed(3, speed);
  }
}

void correction_S(int z_ang) {
  int delta = 10;

  if (z_ang > 3) {
    addy.setSpeed(4, speed + delta);
    addy.setSpeed(1, speed - delta);
  } else if (z_ang < -3) {
    addy.setSpeed(4, speed - delta);
    addy.setSpeed(1, speed + delta);
  } else {
    addy.setSpeed(4, speed);
    addy.setSpeed(1, speed);
  }
}



// float distanceFront = getDistance(trigPinFront, echoPinFront);
  // float distanceBack = getDistance(trigPinBack, echoPinBack);
  // float distanceLeft = getDistance(trigPinLeft, echoPinLeft);
  // float distanceRight = getDistance(trigPinRight, echoPinRight);

  // switch (avoidanceState) {
  //   case NO_OBSTACLE:
  //     // 장애물이 있는지 확인
  //     if (distanceFront <= avoidanceDistance) {
  //       avoidanceState = AVOIDING_BACK;
  //     } else if (distanceBack <= avoidanceDistance) {
  //       avoidanceState = AVOIDING_FRONT;
  //     } else if (distanceRight <= avoidanceDistance) {
  //       avoidanceState = AVOIDING_LEFT;
  //     } else if (distanceLeft <= avoidanceDistance) {
  //       avoidanceState = AVOIDING_RIGHT;
  //     } else {
  //       correction_F();
  //       addy.moveF(200);
  //     }

  //   case AVOIDING_BACK:
  //     if (distanceFront < avoidanceDistance) {
  //       addy.stopAll();

  //       if (distanceRight > distanceLeft && distanceRight > avoidanceDistance) {
  //         addy.rotate(1, 600); // CW
  //         resetAngle();
  //         break;
  //       }
  //       else if (distanceLeft > distanceRight && distanceLeft > avoidanceDistance){
  //         addy.rotate(2, 600); // CCW
  //         resetAngle();
  //         break;
  //       }
  //       else {
  //         addy.moveB(300);
  //         break;
  //       }
  //       break;
  //     }

  //   case AVOIDING_FRONT:
  //     if (distanceBack < avoidanceDistance) {
  //       correction_F();
  //       addy.moveF(300);
  //       // break;
  //     }

  //   case AVOIDING_LEFT:
  //     if (distanceRight < avoidanceDistance) {
  //       correction_S();
  //       addy.moveL(300);
  //       // break;
  //     }

  //   case AVOIDING_RIGHT:
  //     if (distanceLeft < avoidanceDistance) {
  //       correction_S();
  //       addy.moveR(300);
  //       // break;
  //     }
  // }