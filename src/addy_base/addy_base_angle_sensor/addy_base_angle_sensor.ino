#include "./Addy_SmartMobility.h"
#include <SoftwareSerial.h>
#include <Wire.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
float humi, temp;

unsigned long previousMillis = 0;
const long interval = 500; // 5 seconds

float angle[3]={0,}, vec;

int Vo = A1;
int V_LED = 2;  

float Vo_value = 0;
float Voltage = 0;
float dustDensity = 0;

bool displayHumidityTemp = true;

Addy_SmartMobility sm = Addy_SmartMobility();
SoftwareSerial BTSerial(4, 5);

char data;
int speed = 0;
int delta = 0;

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);

  pinMode(A0, INPUT);
  pinMode(V_LED, OUTPUT);
  pinMode(Vo, INPUT);
  
  dht.begin();

  /*if (!sm.begin()) {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1)
      ;
  }*/

  speed = 125;
  sm.setSpeed(speed);
  sm.moveTo(5);

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

int16_t offset[3] = {32, 15, -15};

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

  return atoi(a3);

}

void correction(int cmd) {
  if (cmd == -38) {
    return;
  }
  int z_ang = get_Z();

  delta = 10;
  if (cmd == 2 || cmd == 8) {
    if (z_ang > 1){
      sm.setSpeed(2, speed + delta);
      sm.setSpeed(3, speed - delta);
    }
    else if(z_ang < -1) {
      sm.setSpeed(2, speed - delta);
      sm.setSpeed(3, speed + delta);
    }
    else {
      sm.setSpeed(2, speed);
      sm.setSpeed(3, speed);
    }
  }
    if (cmd == 4 || cmd == 6) {
    if (z_ang > 1){
      sm.setSpeed(4, speed + delta);
      sm.setSpeed(1, speed - delta);
    }
    else if(z_ang < -1) {
      sm.setSpeed(4, speed - delta);
      sm.setSpeed(1, speed + delta);
    }
    else{
      sm.setSpeed(4, speed);
      sm.setSpeed(1, speed);
    }
  }
  /*if (cmd == 2 || cmd == 8) {
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
  }*/
}
void resetAngle() {
  Serial.println("Resetting Angle!");
  for (int i = 0; i < 3; i++) {
    angle[i] = 0;
  }
}

void loop() { 
  int test = get_Z();

  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.equals("4")) {
      resetAngle();
    }
  }
  unsigned long currentMillis = millis();
  int sv = analogRead(A0);
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    temp = dht.readTemperature();
    humi = dht.readHumidity();

    digitalWrite(V_LED, LOW);
    delayMicroseconds(280);
    Vo_value = analogRead(Vo);
    delayMicroseconds(40);
    digitalWrite(V_LED, HIGH);
    delayMicroseconds(9680);

    Voltage = Vo_value * 5.0 / 1023.0;
    dustDensity = (Voltage - 0.3) / 0.005;

    if (isnan(humi) || isnan(temp)) {
      Serial.println("Failed to read from DHT Sensor!!");
      return;
    }
  }
  /*Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print("°C , Humidity: ");
  Serial.print(humi);
  Serial.print("%, CO2: ");
  Serial.print(sv);
  Serial.print("ppm , PM10: ");
  Serial.print(dustDensity);
  Serial.print(" ug/m3");
  Serial.print(", ");*/

  Serial.print("Temperature: ");
  Serial.print(0);
  Serial.print("°C , Humidity: ");
  Serial.print(0);
  Serial.print("%, CO2: ");
  Serial.print(0);
  Serial.print("ppm , PM10: ");
  Serial.print(0);
  Serial.print(" ug/m3");
  Serial.print(", ");
  Serial.println(test);

}