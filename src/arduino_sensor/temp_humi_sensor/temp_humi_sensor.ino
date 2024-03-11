#include <DHT.h>
#include <DHT_U.h>
#include <LiquidCrystal.h>  // 액정 디스플레이 라이브러리

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);  

unsigned long previousMillis = 0;
const long interval = 500; 

void setup() {
  lcd.begin(16, 2);  // 16칸 2줄 LCD 디스플레이 사용
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    float humi, temp;
    temp = dht.readTemperature();
    humi = dht.readHumidity();

    if (isnan(humi) || isnan(temp)) {
      Serial.println("Failed to read from DHT Sensor!!");
      return;
    }

        // 액정화면 표시
    lcd.setCursor(0, 0);
    lcd.print("Humi: "); lcd.print(humi); lcd.print(" %");
    lcd.setCursor(0, 1);
    lcd.print("Temp: "); lcd.print(temp); lcd.print(" C");

    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.print("°C , Humidity: ");
    Serial.print(humi);
    Serial.println("%");
  }
}
