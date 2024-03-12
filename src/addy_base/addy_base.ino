#include "./Addy_SmartMobility.h"
#include <SoftwareSerial.h>
#include "ESP8266.h"

#define SSID "AIE_509_2.4G"
#define PASSWORD "addinedu_class1"
#define HOST_NAME "192.168.0.23"
#define HOST_PORT (8090)

SoftwareSerial mySerial(12, 13); /* RX:13, TX:12 */
ESP8266 wifi(mySerial);

bool tcp_status = false;
Addy_SmartMobility addy = Addy_SmartMobility();

char data;
int speed = 0;
int delta = 0;
int cmd = 0;

void setup() {
  Serial.begin(9600);
  // BTSerial.begin(9600);
  connect_wifi();


  if (!addy.begin()) {
    Serial.println("모터 쉴드 연결을 다시 확인해주세요.");
    while (1)
      ;
  }

  speed = 125;
  addy.setSpeed(speed);
  addy.moveTo(5);
}


void loop() {
  uint8_t buffer[256] = { 0 };

  tcp_on();

  if (tcp_status) {
    char *hello = "Hello, this is client!";
    wifi.send((const uint8_t *)hello, strlen(hello));

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
  addy.moveTo(cmd);
}

void tcp_on() {
  if (wifi.createTCP(HOST_NAME, HOST_PORT)) {
    Serial.print("create tcp ok\r\n");
    tcp_status = true;
  } else {
    Serial.print("create tcp err\r\n");
    tcp_status = false;
  }
}

void tcp_off() {
  if (wifi.releaseTCP()) {
    Serial.print("release tcp ok\r\n");
    tcp_status = false;
  } else {
    Serial.print("release tcp err\r\n");
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
