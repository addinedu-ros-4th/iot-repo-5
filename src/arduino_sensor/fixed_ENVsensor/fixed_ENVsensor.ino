#include <DHT.h>
#include <DHT_U.h>
#include <LiquidCrystal.h>

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);  

unsigned long previousMillis = 0;
const long interval = 5000; // 5 seconds

int red = A0;
int green = A1;
int blue = A2;

int speakerPin = A5;
int Vo = A4;
int V_LED = 7;  

float Vo_value = 0;
float Voltage = 0;
float dustDensity = 0;

bool displayHumidityTemp = true;

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(A3, INPUT);
  pinMode(speakerPin, OUTPUT);
  pinMode(V_LED, OUTPUT);
  pinMode(Vo, INPUT);
  
  dht.begin();
}

void loop() {
  unsigned long currentMillis = millis();
  int sv = analogRead(A3);

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    float humi, temp;
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
    
    if (displayHumidityTemp) {
      lcd.setCursor(0, 0);
      lcd.print("Humi: "); lcd.print(humi); lcd.print(" %");
      lcd.setCursor(0, 1);
      lcd.print("Temp: "); lcd.print(temp); lcd.print(" C");
    } else {
      lcd.setCursor(0, 0);
      lcd.print("CO2: "); lcd.print(sv); lcd.print(" ppm");
      lcd.setCursor(0, 1);
      lcd.print("PM10: "); lcd.print(dustDensity); lcd.print(" ug/m3");
    }

    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.print("°C , Humidity: ");
    Serial.print(humi);
    Serial.print("%, CO2: ");
    Serial.print(sv);
    Serial.print("ppm , PM10: ");
    Serial.print(dustDensity);
    Serial.println(" ug/m3");

    displayHumidityTemp = !displayHumidityTemp; // Toggle the display state
  }
}
