#include <Wire.h>
#include <DHT.h>
#include <DHT_U.h>

#define SLAVE 4
#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);


void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(9600);
  Serial.println("I2C");
  dht.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  i2c_communication();
  delay(100);

  float temp, humi;
  temp = dht.readTemperature();
  humi = dht.readHumidity();

  if (isnan(humi) || isnan(temp)) {
    Serial.println("Failed to read from DHT Sensor!!");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print("°C , Humidity: ");
  Serial.print(humi);
  Serial.println("%");
}


void i2c_communication() {
  Wire.requestFrom(SLAVE, 1);
  char c = Wire.read();
}
