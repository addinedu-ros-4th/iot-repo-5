#include <DHT.h>
#include <DHT_U.h>
#include <LiquidCrystal.h>

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);  

unsigned long previousMillis = 0;
const long interval = 1000;

int red = A0;
int green = A1;
int blue = A2;

int speakerPin = A4;
int Vo = A5;
int V_LED = 7;  

float Vo_value = 0;
float Voltage = 0;
float dustDensity = 0;

bool displayTempHumi = true; 

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

    float co2, pm10;
    co2 = sv; 
    digitalWrite(V_LED, LOW);
    delayMicroseconds(280);
    Vo_value = analogRead(Vo);
    delayMicroseconds(40);
    digitalWrite(V_LED, HIGH);
    delayMicroseconds(9680);

    Voltage = Vo_value * 5.0 / 1024.0;
    dustDensity = (Voltage - 0.1) / 0.005;

    if (displayTempHumi) {
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
      Serial.print("%, CO2: ");
      Serial.print(sv);
      Serial.print("ppm , PM10: ");
      Serial.print(dustDensity);
      Serial.println(" ug/m3");
      
      lcd.clear();
      
      lcd.setCursor(0, 0);
      lcd.print("Temp:"); lcd.print(temp); lcd.print(" C");
      
      lcd.setCursor(0, 1);
      lcd.print("Humi:"); lcd.print(humi); lcd.print(" %");
    } else {
      lcd.clear(); 
      
      lcd.setCursor(0, 0);
      lcd.print("CO2:"); lcd.print(co2); lcd.print(" PPM");
      
      lcd.setCursor(0, 1);
      lcd.print("PM10:"); lcd.print(dustDensity); lcd.print(" ug/m3");
    }

    displayTempHumi = !displayTempHumi; 

    if (dustDensity <= 50.0) {
      analogWrite(red, 0);
      analogWrite(green, 255);
      analogWrite(blue, 0);

      noTone(speakerPin);
    } 
    else if (dustDensity <= 300.0) {
      analogWrite(red, 0);
      analogWrite(green, 0);
      analogWrite(blue, 255);

      noTone(speakerPin);
    }
    else {
      analogWrite(red, 255);
      analogWrite(green, 0);
      analogWrite(blue, 0);

      tone(speakerPin, 1000); 
      delay(500); 
      noTone(speakerPin); 
    }
  }
}
