// #include <HardwareSerial.h>
#include <SoftwareSerial.h>

SoftwareSerial espSerial(2, 3); // rx, tx

void setup() {
  Serial.begin(115200);   // 시리얼 통신 초기화
  espSerial.begin(115200);  // ESP32-CAM의 시리얼 포트 초기화
}

void loop() {
  // Serial.println("Hello, ESP32-CAM! [in arduino]");
  espSerial.println("Hello, ESP32-CAM!");  // ESP32-CAM으로 메시지 전송

  if (espSerial.available()) {                                      // ESP32-CAM으로부터 데이터가 도착하면
    String receivedData = espSerial.readStringUntil('\n');          // 데이터 읽기
    Serial.println("Received from ESP32-CAM : " + receivedData);  // 시리얼 모니터에 출력
  }

  delay(500);
}
