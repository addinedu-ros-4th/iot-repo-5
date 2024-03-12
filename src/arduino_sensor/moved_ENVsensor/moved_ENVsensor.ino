#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 10
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

unsigned long previousMillis = 0;
const long interval = 300; 

int Vo = A2;  
int V_LED = 11; 

float Vo_value = 0;
float Voltage = 0;
float dustDensity = 0;

bool displayHumidityTemp = true;

void setup() {
  Serial.begin(9600);
  
  pinMode(A4, INPUT);
  pinMode(V_LED, OUTPUT);
  pinMode(Vo, INPUT);
  
  dht.begin();
}

void loop() {
  unsigned long currentMillis = millis();
  int sv = analogRead(A4);

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    float humi, temp;
    temp = dht.readTemperature();
    humi = dht.readHumidity();

    digitalWrite(V_LED, LOW);
    Vo_value = analogRead(Vo);
    digitalWrite(V_LED, HIGH);

    Voltage = Vo_value * 5.0 / 1024.0;
    dustDensity = (Voltage - 0.1) / 0.005;

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
  }
}