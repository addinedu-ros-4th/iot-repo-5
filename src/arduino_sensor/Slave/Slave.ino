#include <Wire.h>
#define SLAVE 4

byte count = 'A';
void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE);
  Wire.onRequest(sendToMaster);
}

void loop() {
  // put your main code here, to run repeatedly:
}

void sendToMaster() {
  Wire.write(++count);

}
